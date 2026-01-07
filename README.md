# Introduction


Also for fun, I was recently looking into DIP (Dependency Inversion Principle), so I wanted to use this take-home as a sort of test bench to see how well that would work for this project. Overall, from what I understand we need a pipeline that looks like
```
interfaces  ← domain
     ↑          ↑
application
     ↑
infrastructure
     ↑
wiring / main
```

Here `application only depends on interfaces and domain, infra on application etc. Following this I'll try to build out the whole pipeline and hopefully have a clean ablation on the chunking/retreival stategy later down the line.