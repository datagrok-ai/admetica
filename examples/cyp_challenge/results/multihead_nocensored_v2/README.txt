Negative result: early stopping on the challenge heads only (--monitor-scored).

Hypothesis: E3a's folds stopped at epoch 13-15 because the aggregate val_loss is dominated by the
large auxiliary heads, cutting training before the scored heads converged.

Fold 1, same compounds as results/multihead_nocensored/oof_*_fold1.csv:

  endpoint   E3a      E3a-v2    delta    95% CI
  cyp1a2     0.9044   1.0772   +0.1728  [+0.055,+0.301]
  cyp2c9     0.7702   0.7468   -0.0235  [-0.127,+0.078]
  cyp2d6     1.0020   1.0365   +0.0345  [-0.055,+0.125]
  cyp3a4     0.5920   0.6675   +0.0755  [+0.015,+0.136]
  macro      0.8172   0.8820

Watching only the scored heads makes the stopping signal noisy - those heads carry 1,100-1,900
labels each - and the best epoch landed at 5 rather than 13-15. The aggregate signal was acting as
a stabiliser. The scored heads were not undertrained; fold 2 was not run.
