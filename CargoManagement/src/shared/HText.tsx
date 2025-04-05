import React from "react";

type Props = {
  children: React.ReactNode;
};

const HText = ({ children }: Props) => {
  return (
    <h1 className="text-4xl md:text-6xl font-bold mb-8">
      {children}
    </h1>
  );
};

export default HText;
