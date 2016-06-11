function [T,sigma,sigma2] = allan_2(omega,fs,pts)

[N,M]       = size(omega);
n           = 2.^(0:floor(log2(N/2)))';
maxN        = n(end);
endLogInc   = log10(maxN);
m           = unique(ceil(logspace(0,endLogInc,pts)))';
t0          = 1/fs;
T           = m*t0;

theta       = cumsum(omega) / fs;
sigma2      = zeros(length(T),M);

for i = 1:length(m)
    
    for k = 1:N-2*m(i)
        
        sigma2(i,:) = sigma2(i,:) + ...
                        (theta(k+2*m(i),:) - ...
                        2*theta(k+m(i),:) + ...
                        theta(k,:)).^2;
                    
    end
    
end

sigma2      = sigma2./repmat((2*T.^2.*(N-2*m)),1,M);

sigma       = sqrt(sigma2);

end