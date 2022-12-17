import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns




def pie_chart(data):
    # Plots pie chart of winner based on difficulty

    keys = list(data["WinnerDifficulty"].unique())
    values = []

    keys_bottom_level = []
    values_bottom_level = {"Hard":0, "Normal":0, "Easy":0, "Draw":0}

    explode = [0.0 for i in range(len(keys))]

    # Colors
    colours = {"Normal":plt.cm.Blues, "Hard":plt.cm.Reds, "Easy":plt.cm.Greens, "Draw":plt.cm.Wistia}

    for idx, item in enumerate(keys):
        if item == None:
            values.append(data[(data["WinnerDifficulty"] != "Hard") & (data["WinnerDifficulty"] != "Easy") & (data["WinnerDifficulty"] != "Normal")].shape[0])
            values_bottom_level["Draw"] = values[-1]

        else:
            values.append(data[data["WinnerDifficulty"] == item].shape[0])
            
            value_bottom = {"Easy":0, "Normal":0, "Hard":0}
            for _, row in data[data["WinnerDifficulty"] == item].iterrows():
                if row["Winner"] == "IA":
                    value_bottom[row["P2_Difficulty"]] += 1
                else:
                    value_bottom[row["P1_Difficulty"]] += 1
                    
            values_bottom_level[item] = value_bottom

    if None in keys:
        keys[keys.index(None)] = "Draw"
    
    keys = [x for _,x in sorted(zip(values,keys), reverse=True)]
    values = sorted(values, reverse=True)

    values_2 = []
    keys_2 = []
    for item in keys:
        if item == "Draw":
            values_2.append(values_bottom_level[item])
            keys_2.append(item + "-" + item)
        else:
            for item2 in values_bottom_level[item]:
                if values_bottom_level[item][item2] > 0:
                    values_2.append(values_bottom_level[item][item2])
                    keys_2.append(item + "-" + item2)
    explode2 = [0.00 for i in range(len(keys_2))]

    fig1, ax1 = plt.subplots(figsize=(15, 15))
    
    ax1.pie(values, explode=explode, labels=keys, autopct='%1.1f%%',
            shadow=True, startangle=90, pctdistance=0.85, wedgeprops={"linewidth":1, "edgecolor":"white"}, 
            colors=[colours[item](0.6) for item in keys], labeldistance=1.05,  textprops={"fontsize":18})

    transparency_color = {"Hard":0.1, "Normal":0.25, "Easy":0.35, "Draw":0}
    colours_bottom_level = [colours[item.split("-")[0]](0.6 - transparency_color[item.split("-")[1]]) for item in keys_2]
    sub_labels_2 = [" " for item in keys_2]
    ax1.pie(values_2, explode = explode2, autopct='%1.1f%%',
            shadow=True, labels = sub_labels_2, startangle=90, radius=0.7, pctdistance=0.7, wedgeprops={"linewidth":1, "edgecolor":"white"}, 
            colors=colours_bottom_level, textprops={"fontsize":14})

    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.set_title("Percentage of Wins by Difficulty", weight = "bold", fontsize = 25, y=1.05)

    # Reformat keys 2
    keys_2 = [item.replace("-", " vs. ") for item in keys_2]
    try:
        keys_2[keys_2.index("Draw vs. Draw")] = "Draw"
    except:
        ...

    plt.legend(loc=(0.9,0.1))
    handles, labels = ax1.get_legend_handles_labels()
    ax1.legend(handles[len(keys):], keys_2, loc=(0.9,0.85))


    plt.savefig("GameData/Simulations/PieChart.png")

def histogram(scores_data):
    # Plot density maps and correlation scatterplots

    sns.set_style("dark")

    keys_turns = {"Hard":[], "Normal":[], "Easy":[]}
    keys_scores = {"Hard":[], "Normal":[], "Easy":[]}
    
    for _, row in scores_data.iterrows():

        keys_turns[row["P1_Difficulty"]].append(row["P1_Turns"])
        keys_turns[row["P2_Difficulty"]].append(row["P2_Turns"])

        keys_scores[row["P1_Difficulty"]].append(row["P1_Score"])
        keys_scores[row["P2_Difficulty"]].append(row["P2_Score"])

    
    palette = {"Hard":"tab:red",
        "Easy":"tab:green", 
        "Normal":"tab:cyan"}

    data = {"Scores":[], "Difficulty":[], "Turns":[]}

    for label in keys_scores:
        data["Scores"] = data["Scores"] + keys_scores[label]
        data["Difficulty"] = data["Difficulty"] + [label for i in range(len(keys_scores[label]))]
        data["Turns"] = data["Turns"] + keys_turns[label]


    df = pd.DataFrame(data, columns=["Scores", "Turns", "Difficulty"])

    # Density Plot of Scores
    ax = sns.displot(df, x="Scores", hue="Difficulty", kind="kde", palette=palette, fill = True, height=10, aspect=15/10)
    plt.title("Distribution of Scores based on Difficulty")
    plt.xlabel("Score")
    # plt.xlim(0, 15) Això és per si no volem nombres negatius o superior al maxim, no es que esitgui incorrecte l'original
    # https://stats.stackexchange.com/questions/109549/negative-density-for-non-negative-variables
    sns.move_legend(ax, "center right")

    # What is kde:
    # A kernel density estimate (KDE) plot is a method for visualizing the distribution of observations 
    # in a dataset, analogous to a histogram. KDE represents the data using a 
    # continuous probability density curve in one or more dimensions.
    plt.savefig("GameData/Simulations/HistogramScores.png", bbox_inches='tight')



    # Density plot of turns
    ax = sns.displot(df, x="Turns", hue="Difficulty", kind="kde", fill = True, palette=palette, height=10, aspect=15/10)
    plt.title("Distribution of Turns based on Difficulty")
    plt.xlabel("Turns")
    sns.move_legend(ax, "center right")
    plt.savefig("GameData/Simulations/HistogramTurns.png", bbox_inches='tight')

    


    # Scatter plot of Turns & Scores
    for label in palette:
        plt.scatter(y = df[df["Difficulty"]==label]["Turns"], x = df[df["Difficulty"]==label]["Scores"], alpha=0.2, color=palette[label])
        plt.annotate(label, 
                 df.loc[df['Difficulty']==label,['Scores','Turns']].mean(),
                 horizontalalignment='center',
                 verticalalignment='center',
                 size=20, weight='bold',
                 color=palette[label]) 
    plt.xlabel("Score")
    plt.ylabel("Turn")
    plt.title("Correlation between Score & Turn by Difficulty")
    plt.savefig("GameData/Simulations/CorrelationTurnsScores.png", bbox_inches='tight')
    

if __name__ == "__main__":
    # 10 max torns i 15 max score
    match_results = pd.read_pickle("GameData/Simulations/match_results_data.pkl")
    #match_data = pd.read_pickle("GameData/Simulations/match_complete_data.pkl")

    pie_chart(match_results)
    histogram(match_results)