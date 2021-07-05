# import pandas
import pandas as pd
from matplotlib import pyplot as plt

# Carpentries link for gapminder data
data_url = 'http://bit.ly/2cLzoxH'
# load gapminder data from url as pandas dataframe
gapminder = pd.read_csv(data_url)
gapminder_us = gapminder[gapminder.country == "United States"]

# create figure and axis objects
fig, ax = plt.subplots()
ax.plot(gapminder_us.year, gapminder_us.lifeExp, color="red", marker="o")
ax.set_xlabel("year", fontsize=14)
ax.set_ylabel("lifeExp", color="red", fontsize=14)

# twin object for two different y-axis on the sample plot
ax2 = ax.twinx()
ax2.plot(gapminder_us.year, gapminder_us["gdpPercap"], color="blue", marker="o")
ax2.set_ylabel("gdpPercap", color="blue", fontsize=14)
# save the plot as a file
fig.savefig('two_different_y_axis_for_single_python_plot_with_twinx.jpg',
            format='jpeg',
            dpi=100,
            bbox_inches='tight')

