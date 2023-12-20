#include "KalmanFilter.h"

KalmanFilter::KalmanFilter(float Q, float R, float P, float X) {
  this->Q = Q;
  this->R = R;
  this->P = P;
  this->X = X;
}

float KalmanFilter::update(float measurement) {
  // Prediction step
  this->P = this->P + this->Q;

  // Kalman gain calculation
  float K = this->P / (this->P + this->R);

  // Update step
  this->X = this->X + K * (measurement - this->X);
  this->P = (1 - K) * this->P;

  return this->X;
}