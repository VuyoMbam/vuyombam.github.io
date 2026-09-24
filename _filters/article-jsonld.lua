-- Adds schema.org Article structured data (JSON-LD) to every article in posts/.
--
-- Registered for the whole posts/ folder in posts/_metadata.yml, so a new article gets it
-- with no extra work. It tells search engines this page is an article by the person the
-- homepage describes (the author is the same Person entity, "<site>/#person").
--
-- Reads:
--   * the article's own front matter (title, description, date, date-modified, categories,
--     image) straight from its .qmd, because by the time filters run Quarto has already
--     turned the date into display text such as "September 24, 2026";
--   * data/profile.yml for the site URL, the author's name and the default image.
-- Invisible on the page. Only public facts go in.

local function read_file(path)
  local f = io.open(path, "rb")
  if not f then return nil end
  local s = f:read("*a")
  f:close()
  return s
end

-- Parse the YAML block at the top of a file into pandoc metadata.
local function front_matter(path)
  local text = read_file(path)
  if not text then return nil end
  text = text:gsub("\r\n", "\n")
  local yaml = text:match("^%-%-%-\n(.-)\n%-%-%-\n")
  if not yaml then return nil end
  return pandoc.read("---\n" .. yaml .. "\n---\n", "markdown-smart").meta
end

-- Parse a plain YAML file (no --- fences) into pandoc metadata.
local function yaml_file(path)
  local text = read_file(path)
  if not text then return nil end
  text = text:gsub("\r\n", "\n")
  return pandoc.read("---\n" .. text .. "\n---\n", "markdown-smart").meta
end

local function str(v)
  if v == nil then return nil end
  local s = pandoc.utils.stringify(v)
  if s == "" then return nil end
  return s
end

local MONTHS = { January = 1, February = 2, March = 3, April = 4, May = 5, June = 6, July = 7,
                 August = 8, September = 9, October = 10, November = 11, December = 12 }

-- "2026-09-24" stays as is; "September 24, 2026" becomes "2026-09-24".
local function iso_date(s)
  if not s then return nil end
  local y, m, d = s:match("^(%d%d%d%d)%-(%d%d)%-(%d%d)")
  if y then return y .. "-" .. m .. "-" .. d end
  local mon, day, year = s:match("^(%a+)%s+(%d+),%s*(%d%d%d%d)")
  if mon and MONTHS[mon] then
    return string.format("%04d-%02d-%02d", tonumber(year), MONTHS[mon], tonumber(day))
  end
  return s
end

function Pandoc(doc)
  if not FORMAT:match("html") then return nil end

  local project = quarto and quarto.project and quarto.project.directory
  local input = quarto and quarto.doc and quarto.doc.input_file
  if not project or not input then return nil end

  local article = front_matter(input)
  local site_meta = yaml_file(project .. "/data/profile.yml")
  if not article or not site_meta or not site_meta.profile then
    io.stderr:write("[article-jsonld] skipped: article=" .. tostring(article ~= nil) ..
      " (" .. tostring(input) .. ") profile=" .. tostring(site_meta ~= nil and site_meta.profile ~= nil) ..
      " (" .. tostring(project) .. "/data/profile.yml)\n")
    return nil
  end

  local profile = site_meta.profile
  local site = str(profile.site_url):gsub("/+$", "")
  local person_id = site .. "/#person"
  local slug = pandoc.path.filename(pandoc.system.get_working_directory())
  local url = site .. "/posts/" .. slug .. "/"

  local title = str(article.title)
  if not title then return nil end

  -- image: absolute stays, "/x.png" is from the site root, "x.png" sits beside the article
  local image = str(article.image)
  if not image then
    image = str(profile.image)
  end
  if image and not image:match("^https?://") then
    if image:sub(1, 1) == "/" then
      image = site .. image
    else
      image = url .. image
    end
  end

  local published = iso_date(str(article.date))
  local modified = iso_date(str(article["date-modified"])) or published

  local keywords = nil
  if article.categories then
    local names = {}
    if pandoc.utils.type(article.categories) == "List" then
      for _, c in ipairs(article.categories) do names[#names + 1] = str(c) end
    else
      names[1] = str(article.categories)
    end
    if #names > 0 then keywords = table.concat(names, ", ") end
  end

  local data = {
    ["@context"] = "https://schema.org",
    ["@type"] = "Article",
    ["@id"] = url .. "#article",
    headline = title,
    description = str(article.description),
    url = url,
    mainEntityOfPage = { ["@type"] = "WebPage", ["@id"] = url },
    datePublished = published,
    dateModified = modified,
    image = image and { image } or nil,
    keywords = keywords,
    inLanguage = "en",
    author = { ["@type"] = "Person", ["@id"] = person_id, name = str(profile.name), url = site .. "/" },
    publisher = { ["@id"] = person_id },
    isPartOf = { ["@id"] = site .. "/#website" },
  }

  local payload = pandoc.json.encode(data)
  payload = payload:gsub("</", "<\\/")     -- never let text close the script tag
  doc.blocks:insert(pandoc.RawBlock("html",
    '<script type="application/ld+json">' .. payload .. "</script>"))
  return doc
end
