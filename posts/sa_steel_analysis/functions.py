import matplotlib.pyplot as plt

provinces = ["Western Cape", "Eastern Cape", "Northern Cape", "North West", "Gauteng", 
             "Mpumalanga", "Limpopo", "Free State", "KwaZulu-Natal"]

district_munics = ['West Coast (DC1)',
       'Cape Winelands (DC2)', 'Overberg (DC3)', 'Eden (DC4)',
       'Central Karoo (DC5)', 'City of Cape Town (CPT)',
       'Sarah Baartman (DC10)', 'Amathole (DC12)', 'Chris Hani (DC13)',
       'Joe Gqabi (DC14)', 'O.R.Tambo (DC15)', 'Alfred Nzo (DC44)',
       'Buffalo City (BUF)', 'Nelson Mandela Bay (NMA)',
       'Namakwa (DC6)', 'Pixley ka Seme (DC7)', 'Z F Mgcawu (DC8)',
       'Frances Baard (DC9)', 'John Taolo Gaetsewe (DC45)',
       'Xhariep (DC16)', 'Lejweleputswa (DC18)',
       'Thabo Mofutsanyane (DC19)', 'Fezile Dabi (DC20)',
       'Mangaung (MAN)', 'Ugu (DC21)',
       'UMgungundlovu (DC22)', 'Uthukela (DC23)', 'Umzinyathi (DC24)',
       'Amajuba (DC25)', 'Zululand (DC26)', 'Umkhanyakude (DC27)',
       'King Cetshwayo (DC28)', 'iLembe (DC29)', 'Harry Gwala (DC43)',
       'eThekwini (ETH)', 'Bojanala (DC37)',
       'Ngaka Modiri Molema (DC38)', 'Dr Ruth Segomotsi Mompati (DC39)',
       'Dr Kenneth Kaunda (DC40)', 'Sedibeng (DC42)',
       'West Rand (DC48)', 'Ekurhuleni (EKU)',
       'City of Johannesburg (JHB)', 'City of Tshwane (TSH)',
       'Gert Sibande (DC30)', 'Nkangala (DC31)',
       'Ehlanzeni (DC32)', 'Mopani (DC33)', 'Vhembe (DC34)',
       'Capricorn (DC35)', 'Waterberg (DC36)',
       'Greater Sekhukhune (DC47)']

def plot_maps(geo_df, indicator:str , industries: list):
    fig, axs = plt.subplots(1,len(industries), sharex=True, sharey=True, 
                            figsize=(9,9),
                            constrained_layout=True,
                            subplot_kw=dict(aspect='equal'),
                            dpi=300)

    if len(industries) > 1:
        axs = axs.ravel()
        for idx in range(len(industries)):
            geo_df.plot(
                column = industries[idx], 
                cmap='BuPu',
                linewidth = 0.5,
                edgecolor='black',
                ax=axs[idx],
                # legend=True,

                # legend_kwds={'orientation':'horizontal', 'label':f'Output [R"million"]', 'location':'bottom'}
                )
            
            cbar = plt.colorbar(axs[idx].collections[0], ax = axs[idx], location='bottom', shrink = 0.7)
            cbar.ax.set_title(f'{indicator} [R million]', fontdict={'fontsize':6})
            cbar.ax.tick_params(labelsize=4)
            
            axs[idx].set_title(f"\n\n{industries[idx]}", fontsize=6, wrap=True, loc='center', fontweight='bold')
            axs[idx].set_axis_off()
            geo_df.apply(lambda x: axs[idx].annotate(text=x['DISTRICT_N'], xy=x.geometry.centroid.coords[0], ha='center', fontsize=6), axis=1)
    else:
        geo_df.plot(
            column = industries[0], 
            cmap='BuPu',
            linewidth = 0.5,
            edgecolor='black',
            ax=axs,
            # legend=True,

            # legend_kwds={'orientation':'horizontal', 'label':f'Output [R"million"]', 'location':'bottom'}
            )
        
        cbar = plt.colorbar(axs.collections[0], ax = axs, location='bottom', shrink = 0.7)
        cbar.ax.set_title(f'{indicator} [R million]', fontdict={'fontsize':6})
        cbar.ax.tick_params(labelsize=4)
        
        axs.set_title(f"\n\n{industries[0]}", fontsize=6, wrap=True, loc='center', fontweight='bold')
        axs.set_axis_off()
        geo_df.apply(lambda x: axs.annotate(text=x['DISTRICT_N'], xy=x.geometry.centroid.coords[0], ha='center', fontsize=6), axis=1)
        
        
    plt.figtext(s='\n\n\nCSIR Analysis', x=0, y=-0.03, fontstyle='italic', fontsize = 4).set_verticalalignment(align='bottom')