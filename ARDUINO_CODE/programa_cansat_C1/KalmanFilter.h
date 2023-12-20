#ifndef KALMAN_FILTER_H
#define KALMAN_FILTER_H

class KalmanFilter {
  public:
    KalmanFilter(float Q, float R, float P, float X);

    float update(float measurement);

  private:
    float Q;
    float R;
    float P;
    float X;
};

#endif
