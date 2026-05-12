library(tidyverse)
library(lpSolve)

summary_table <- read.csv("data/processed/summary_table.csv")

assets <- summary_table$Asset
returns_vec <- summary_table$Expected_Return
risk_vec <- summary_table$Risk
n <- length(assets)

f.obj <- returns_vec

f.con <- rbind(
  rep(1, n),
  risk_vec,
  diag(n)
)

f.dir <- c("=", "<=", rep("<=", n))

risk_limit <- 0.030
max_allocation <- 0.30

f.rhs <- c(
  1,
  risk_limit,
  rep(max_allocation, n)
)

portfolio.sol <- lp(
  direction = "max",
  objective.in = f.obj,
  const.mat = f.con,
  const.dir = f.dir,
  const.rhs = f.rhs
)

allocation_table <- summary_table %>%
  mutate(
    Allocation = portfolio.sol$solution,
    Dollar_Allocation = Allocation * 100000
  )

write.csv(allocation_table, "data/processed/allocation_table.csv", row.names = FALSE)

print(allocation_table)
print(portfolio.sol$objval)
