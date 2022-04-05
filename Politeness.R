
library(politeness)

install.packages("spacyr")
library("spacyr")
spacy_install()
spacy_initialize()

techSupport <- clean_techsupport$text

tech_polite = colMeans(politeness(techSupport, parser="spacy", metric="count", drop_blank=FALSE))
graphData <- c(tech_polite["Positive.Emotion"],tech_polite["Negative.Emotion"],tech_polite["Please"],tech_polite["Gratitude"]
               ,tech_polite["Apology"],tech_polite["Swearing"])

barplot(graphData, space = c(3,4,3.5,2,2,2), xlab="Politeness Feature(clean techsupport data)", ylab="Average Value")


mentalHealth <- clean_mentalhealth$text

mentalHealth_polite = colMeans(politeness(mentalHealth, parser="spacy", metric="count", drop_blank=FALSE))
graphData2 <- c(mentalHealth_polite["Positive.Emotion"],mentalHealth_polite["Negative.Emotion"],mentalHealth_polite["Please"]
               ,mentalHealth_polite["Gratitude"]
               ,mentalHealth_polite["Apology"]
               ,mentalHealth_polite["Swearing"])

barplot(graphData2, space = c(3,4,3.5,2,2,2), xlab="Politeness Feature(clean mentalhealth data)", ylab="Average Value")

