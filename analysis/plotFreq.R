#setwd("/Users/winteram/Documents/Research/FashionPins")

library(ggplot2)
library(cluster)
theme_set(theme_bw())

pin.srcs <- read.csv("frequency.csv", header=FALSE)
names(pin.srcs) <- c("Source","Freq")

ggplot(pin.srcs, aes(x=Freq)) + geom_histogram(color="black", fill="white") + scale_y_log10()

simmat <- read.csv("simmat.csv", header=TRUE)
simmat2 <- read.csv("simmat2.csv", header=FALSE)
simmat.mat <- as.matrix(simmat2.csv)

# user by user
c <- simmat.mat %*% t(simmat.mat)  # N x M * M x N
kmc <- kmeans(c,3)
clusters <- kmc$cluster
clusplot(c, clusters, cor=FALSE, color=TRUE, shade=TRUE, labels=2, lines=0)

pc.cr <- princomp(c)
plot(pc.cr)

# source by source
d <- t(simmat.mat) %*% simmat.mat  # M x N * N x M
kmd <- kmeans(d,3)
clusters <- kmd$cluster
clusplot(d, clusters, cor=FALSE, color=TRUE, shade=TRUE, labels=2, lines=0)


