
library(entropy)
library(RColorBrewer)
library(ggplot2)
library(jsonlite)


setwd("C:/Users/delif/Documents/source/repos/LeagueOfLegendsHeatMap")
df <- read.table("heatMapData.txt", sep = ",", col.names = c('X', 'Y'), strip.white = TRUE)

# separate X and Y values for discretizing function
xValues <- df$X
yValues <- df$Y

# discretize values and transform to dataframe
binnedData <- discretize2d(xValues, yValues, numBins1 = 128, numBins2 = 128, r1 = c(-120,14780), r2 = c(-120,14980))
binnedDataDF <- as.data.frame(binnedData)
colnames(binnedDataDF) <- c('X', 'Y', 'freq')

# write data to JSON file
jsonData <- toJSON(binnedDataDF)
write(jsonData, "heatmap_data.json")


# create color palette
rf <- colorRampPalette(rev(brewer.pal(11,'Spectral')))
r <- rf(32)

# plot discretized data using log scale
p <- ggplot(df, aes(x=xValues, y=yValues)) + stat_bin2d(bins=128) + scale_fill_gradientn(colors=r, trans='log') + coord_fixed()

# save plot as SVG
svg("heatmap.svg", width=8, height=8)
print(p)
dev.off()
