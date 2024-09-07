import React from 'react';

const CardHeader = ({ children, className }) => {
  return (
    <div className={`text-xl font-bold mb-2 ${className}`}>
      {children}
    </div>
  );
};

export default CardHeader;
