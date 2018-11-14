rm(list=objects())
setwd("~/")

###############################################
### Q1
###############################################

df=read.table("~/Centrale-DM.data",dec=".",header=TRUE)
colnames(df)[which(names(df) == "extra1")] <- "ABS"

###############################################
### Q2
###############################################

#png(file = "scatterplot_matrices.png")

### En utilisant x11(), on peut ouvrir une nouvelle fen¨ºtre

x11()
pairs(~price+age+km+TIA,data = df,
      main = "Scatterplot Matrix")
dev.off()

### Avec le graphe Scatterplot, on peut voir des relations presquement lin¨¦aire entre 
### (price, age), (price, km) et (age, km)

x11()
par(mfrow=c(1,2))

boxplot(price~ABS,data=df, main="Boxplot: price - ABS",
        xlab="ABS", ylab="price") 

### lorsque ABS = 1, le 1/2-quantile de price est plus grand que celui de ABS = 0, mais il y a plus de 
### donn¨¦es aberrantes qui sont en dehors de bornes. 

boxplot(price~extra2,data=df, main="Boxplot: price - option de toit ouvrant",
        xlab="option de toit ouvrant", ylab="price") 
dev.off()

### les propri¨¦t¨¦s sont similaires au graph pr¨¦c¨¦dent, mais les deux 1/2-quantiles sont plus proches.

###############################################
### Q3
###############################################

### NON! c'est parce que dans le cas ici, les valeurs possibles de ABS ne sont que (0,1) 
### qui est la m¨ºme chose pour les 2 cas

x11()
plot(df$ABS, df$price, xlab="ABS", ylab="price", xlim=c(-1,2))
abline(lm(price ~ ABS, data = df)) 
dev.off()

### Avec la r¨¦gression simple, on peut trouver que la ligne passe par les deux moyens pour ABS = 0 et
### ABS = 1

###############################################
### Q4(a)
###############################################

model = lm(price~km, data = df)
summary(model)
x11()
plot(df$km, df$price, xlab="km", ylab="price", main= "linear Regression: price - km")
abline(model) 
dev.off()

### Coefficients:
### Estimate Std. Error t value Pr(>|t|)    
### (Intercept)  5.559202   0.247970  22.419   <2e-16 ***
###  km          -0.016051   0.001747  -9.187   <2e-16 ***

### Pr(>|t|) est assez petit, on peut ainsi dire qu'il y a une relation lineaire entre les variables.

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

### on a km.centered.scaled = kop1, avec une valeur de covariant tr¨¨s proche ¨¤ 1
### Th¨¦oriquement, on a X1*theta1 = (inverse[((X-u)/delta)*((X-u)/delta)'*((X-u)/delta)])*((X-u)/delta)'*Y
### d'o¨´ le r¨¦sultat

###############################################
### Q4(d)
###############################################

model2 = lm(price~km + I(km^2) + I(km^3), data=df)
summary(model2)

### se r¨¦f¨¦rer dans le rapport pour le mod¨¨le
### oui, on peut le consid¨¦rer comme un mod¨¨le lin¨¦aire, vu que l'on simplifier km^2 et km^3 comme X2 et X3
### par les graphes de mod¨¨le, on sait que ce mod¨¨le est mieux que lm(price~km, data = df)

###############################################
### Q4(e)
###############################################

model3 = lm(price~I(km^3) + I(km^2)+ km, data=df)
anova(model2)

# Analysis of Variance Table
# 
# Response: price
# Df  Sum Sq Mean Sq F value  Pr(>F)    
# km          1  88.086  88.086 87.9058 < 2e-16 ***
#   I(km^2)     1   9.007   9.007  8.9883 0.00313 ** 
#   I(km^3)     1   0.089   0.089  0.0891 0.76573    
# Residuals 168 168.345   1.002                    

anova(model3)

# Analysis of Variance Table
# 
# Response: price
# Df  Sum Sq Mean Sq F value    Pr(>F)    
# I(km^3)     1  57.721  57.721 57.6030 2.104e-12 ***
#   I(km^2)     1  37.166  37.166 37.0896 7.444e-09 ***
#   km          1   2.295   2.295  2.2906     0.132    
# Residuals 168 168.345   1.002              

### NON, parce que les variables explicatives ne sont pas orthogonales ici

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

### les variables explicatives ne sont pas orthogonales ici, ce qui influencie beaucoup les estimateurs
### vif est assez grand
#Xj est corr¨¦l¨¦e lin¨¦airement aux autres variables
### plus pr¨¦cis¨¦ment, se r¨¦f¨¦rer dans le rapport

###############################################
### Q4(g)
###############################################

df$kop1%*%df$kop2
# [,1]
# [1,] -3.29999e-08
df$kop1%*%df$kop3
# [,1]
# [1,] 9.582808e-07
df$kop2%*%df$kop3
# [,1]
# [1,] -5.508632e-07

#proches de 0

df$kop1 - scale(df$kop1, center = T, scale = T)
df$kop2 - scale(df$kop2, center = T, scale = T)
df$kop3 - scale(df$kop3, center = T, scale = T)

model5 = lm(price~kop1 + kop2 + kop3, data=df)
summary(model5)

# Coefficients:
#   Estimate Std. Error t value Pr(>|t|)    
# (Intercept)  3.39654    0.07633  44.500  < 2e-16 ***
#   kop1        -0.71563    0.07633  -9.376  < 2e-16 ***
#   kop2         0.22883    0.07633   2.998  0.00313 ** 
#   kop3         0.02278    0.07633   0.298  0.76573

### on voit que kop1 et kop2 sont des varibales significatives


### Combinaison Lineaire de km, km^2, km^3 et 1

A = matrix(c(df$km[1],((df$km)^2)[1],((df$km)^3)[1],1,
             df$km[2],((df$km)^2)[2],((df$km)^3)[2],1,
             df$km[3],((df$km)^2)[3],((df$km)^3)[3],1,
             df$km[4],((df$km)^2)[4],((df$km)^3)[4],1),
             nrow=4, ncol=4, byrow = TRUE)

solution1 = solve(A)%*%df$kop1[1:4]
solution2 = solve(A)%*%df$kop2[1:4]
solution3 = solve(A)%*%df$kop3[1:4]

### kop et km sont dans le m¨ºme espace, il ne nous faut v¨¦rifier la relation compinaison lin¨¦aire entre eux.

solution1[1]*(df$km) + solution1[2]*((df$km)^2) + solution1[3] * ((df$km)^3) + solution1[4] * c(1,1,1,1)
solution2[1]*(df$km) + solution2[2]*((df$km)^2) + solution2[3] * ((df$km)^3) + solution2[4] * c(1,1,1,1)
solution3[1]*(df$km) + solution3[2]*((df$km)^2) + solution3[3] * ((df$km)^3) + solution2[4] * c(1,1,1,1)

### les valeurs en dessus sont bien ¨¦gales ¨¤ celles de kop1, kop2 et kop3, notre mod¨¨le est bien justifi¨¦

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

# Il est possible d'effectuer la r¨¦gression polynomiale d'ordre 3 en utilisant les
# variables kop1, kop2 et kop3 qui sont orthogonales et engendrent le m¨ºme espace
# que km, km^2 et km^3.C'est pourquoi les 3 formules en dessus sont statistiquement ¨¦quivalentes.

### Method stepwise by stepAIC backward

library(MASS)
backward=stepAIC(model.final1, direction = "backward")
class(backward)
backward$coef
backward$anova

# Final Model:
#   price ~ km + I(km^2) + age + I(age^3)


### Method stepwise by stepAIC both

both=stepAIC(model.final1, direction = "both")
class(both)
both$coef
both$anova

# Final Model:
#   price ~ km + I(km^2) + age + I(age^3)


### Method stepwise by stepAIC forward avec d¨¦but de chaine ¨¤ km

forward=stepAIC(lm(price~km, data = df), direction = "forward", 
                scope = list(upper = model.final1, lower = lm(price~km, data = df)))
class(forward)
forward$coef
forward$anova

# Final Model:
#   price ~ km + ageop1 + I(age^3) + I(km^3)



### Method Leaps, minimiser la valeur de 'Cp'

library(leaps)
leaps=regsubsets(price~TIA+ABS+extra2+kop1+kop2+kop3+ageop1+ageop2+ageop3, data=df, nbest=2)

x11()
subsets(leaps,statistic = "cp")

########     il faudrait cliquer un point dans le graphe pour continuer la programmation

abline(1,1,lty=2,col="red")
dev.off

### On peut ainsi chosir "kop1 ageop1 ageop2","ABS k1 a1 a2" comme les variables explicatives

###############################################
### Q5(b)
###############################################

anova(backward, model.final1)

# Res.Df    RSS Df Sum of Sq      F Pr(>F)
# 1    167 91.369                           
# 2    162 90.721  5   0.64799 0.2314 0.9483

anova(forward, model.final1)

# Res.Df    RSS Df Sum of Sq      F Pr(>F)
# 1    167 91.342                           
# 2    162 90.721  5   0.62141 0.2219 0.9527

anova(both, model.final1)

# Res.Df    RSS Df Sum of Sq      F Pr(>F)
# 1    167 91.369                           
# 2    162 90.721  5   0.64799 0.2314 0.9483

### les 3 valeurs de Pr(>F) sont tr¨¨s proche de 1, c¨¤d les surmod¨¨les sont bien optimis¨¦s et valid¨¦s.



