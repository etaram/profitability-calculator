import React from 'react';

const CardContent = ({ children, className }) => {
  return (
    <div className={`text-gray-700 ${className}`}>
      {children}
    </div>
  );
};

export default CardContent;
