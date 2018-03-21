function [J, grad] = costFunctionReg(theta, X, y, lambda)
%COSTFUNCTIONREG Compute cost and gradient for logistic regression with regularization
%   J = COSTFUNCTIONREG(theta, X, y, lambda) computes the cost of using
%   theta as the parameter for regularized logistic regression and the
%   gradient of the cost w.r.t. to the parameters. 

% Initialize some useful values
m = length(y); % number of training examples

% You need to return the following variables correctly 
J = 0;
grad = zeros(size(theta));

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost of a particular choice of theta.
%               You should set J to the cost.
%               Compute the partial derivatives and set grad to the partial
%               derivatives of the cost w.r.t. each parameter in theta

theta_l = size(theta,1);
reg_exp = (lambda/(2*m))*sum((theta.^2)(2:theta_l));

J = -(1/m)*(y'*log(sigmoid(X*theta))+(1-y)'*log(1-sigmoid(X*theta))) + reg_exp;

for j = 1:theta_l,
  if j == 1,
    grad(j) = (1/m)*(X(:,j)'*(sigmoid(X*theta)-y));
  else
    grad(j) = (1/m)*(X(:,j)'*(sigmoid(X*theta)-y)) + (lambda/m)*theta(j);
  end;
end; 



% =============================================================

end
