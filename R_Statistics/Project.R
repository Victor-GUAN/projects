rm(list=objects())
setwd("F:/ECP Ann¨¦e 1/Stat. Avan/DM")

###############################################
### Q1
###############################################

df=read.table("F:/ECP Ann¨¦e 1/Stat. Avan/DM/Centrale-DM.data",dec=".",header=TRUE)
colnames(df)[which(names(df) == "extra1")] <- "ABS"

###############################################
### Q2
###############################################

#png(file = "scatterplot_matrices.png")

x11()
pairs(~price+age+km+TIA,data = df,
      main = "Scatterplot Matrix")
dev.off()

x11()
par(mfrow=c(1,2))

boxplot(price~ABS,data=df, main="Boxplot: price - ABS",
        xlab="ABS", ylab="price") 

boxplot(price~extra2,data=df, main="Boxplot: price - option de toit ouvrant",
        xlab="option de toit ouvrant", ylab="price") 
dev.off()

###############################################
### Q3
###############################################

x11()
plot(df$ABS, df$price, xlab="ABS", ylab="price", xlim=c(-1,2))
abline(glm(price ~ ABS, data = df)) 
dev.off()

###############################################
### Q4(a)
###############################################

model = lm(price~km, data = df)
summary(model)
x11()
plot(df$km, df$price, xlab="km", ylab="price", main= "linear Regression: price - km")
abline(model) 
dev.off()

###############################################
### Q4(b)
###############################################

predict(model,newdata=data.frame(km=50),
        interval="confidence")

# fit      lwr      upr
#  4.756639 4.426392 5.086886

predict(model,newdata=data.frame(km=135),
        interval="confidence")

# fit      lwr      upr
#  3.392284 3.238505 3.546063

# Simplement, 5.09-4.43 != 3.55-3.24


###############################################
### Q4(c)
###############################################

N = dim(df)[1]
km.centered.scaled <- scale(df$km, center = T, scale = T)*sqrt(N/(N-1))
cov(df$kop1, km.centered.scaled)

###############################################
### Q4(d)
###############################################

model2 = lm(price~km + I(km^2) + I(km^3), data=df)
summary(model2)

###############################################
### Q4(e)
###############################################

model3 = lm(price~I(km^3) + I(km^2)+ km, data=df)
anova(model2)
anova(model3)

###############################################
### Q4(f)
###############################################

vif.km=1/(1-summary(lm(km ~ I(km^2) + I(km^3),data=df))$r.squared)

vif.km2=1/(1-summary(lm(I(km^2) ~ km + I(km^3),data=df))$r.squared)

vif.km3=1/(1-summary(lm(I(km^3) ~ km + I(km^2),data=df))$r.squared)

library(car)
model4 = lm(price ~ km + I(km^2) + I(km^3), data=df)
summary(model4)

# checking multicolinearity for independent variables.
vif(model4)

###############################################
### Q4(g)
###############################################

df$kop1%*%df$kop2
df$kop1%*%df$kop3
df$kop2%*%df$kop3

df$kop1 - scale(df$kop1, center = T, scale = T)
df$kop2 - scale(df$kop2, center = T, scale = T)
df$kop3 - scale(df$kop3, center = T, scale = T)

model5 = lm(price~kop1 + kop2 + kop3, data=df)
summary(model5)


### Combinaison Lineaire de km, km^2, km^3 et 1

A = matrix(c(df$km[1],((df$km)^2)[1],((df$km)^3)[1],1,
             df$km[2],((df$km)^2)[2],((df$km)^3)[2],1,
             df$km[3],((df$km)^2)[3],((df$km)^3)[3],1,
             df$km[4],((df$km)^2)[4],((df$km)^3)[4],1),
             nrow=4, ncol=4, byrow = TRUE)

solution1 = solve(A)%*%df$kop1[1:4]
solution2 = solve(A)%*%df$kop2[1:4]
solution3 = solve(A)%*%df$kop3[1:4]

solution1[1]*(df$km) + solution1[2]*((df$km)^2) + solution1[3] * ((df$km)^3) + solution1[4] * c(1,1,1,1)
solution2[1]*(df$km) + solution2[2]*((df$km)^2) + solution2[3] * ((df$km)^3) + solution2[4] * c(1,1,1,1)
solution3[1]*(df$km) + solution3[2]*((df$km)^2) + solution3[3] * ((df$km)^3) + solution2[4] * c(1,1,1,1)

###############################################
### Q5(a)
###############################################

colnames(df)
model.final1 = lm(price ~ km + I(km^2) + I(km^3) + age + I(age^2) + I(age^3) + 
                   TIA + ABS + extra2 + kop1 + kop2 + kop3 + ageop1 + ageop2 + ageop3, data = df)
model.final2 = lm(price ~ 
                   TIA + ABS + extra2 + kop1 + kop2 + kop3 + ageop1 + ageop2 + ageop3, data = df)
model.final3 = lm(price ~., data = df)

summary(model.final1)
summary(model.final2)
summary(model.final3)

### Method stepwise by stepAIC

library(MASS)
backward=stepAIC(model.final1, direction = "backward")
class(backward)
backward$coef
backward$anova

both=stepAIC(model.final1, direction = "both")
class(both)
both$coef
both$anova

forward=stepAIC(lm(price~km, data = df), direction = "forward", 
                scope = list(upper = model.final1, lower = lm(price~km, data = df)))
class(forward)
forward$coef
forward$anova

library(leaps)
leaps=regsubsets(price~TIA+ABS+extra2+kop1+kop2+kop3+ageop1+ageop2+ageop3, data=df, nbest=2)

x11()
subsets(leaps,statistic = "cp")
abline(1,1,lty=2,col="red")
dev.off

### On peut ainsi chosir "kop1 ageop1 ageop2","ABS k1 a1 a2" comme les variables explicatives

###############################################
### Q5(b)
###############################################

anova(backward, model.final1)
anova(forward, model.final1)
anova(both, model.final1)



