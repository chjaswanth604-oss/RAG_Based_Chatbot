import React, { useState, useEffect } from 'react';
import { Bot, Search, Sparkles } from 'lucide-react';

const Loading = () => {
  const [step, setStep] = useState(0);

  const steps = [
    { text: "Searching college knowledge base...", icon: Search },
    { text: "Matching document vectors...", icon: Sparkles },
    { text: "Generating verified RAG response...", icon: Bot }
  ];

  useEffect(() => {
    const timer1 = setTimeout(() => setStep(1), 1200);
    const timer2 = setTimeout(() => setStep(2), 2400);
    return () => {
      clearTimeout(timer1);
      clearTimeout(timer2);
    };
  }, []);

  const CurrentIcon = steps[step].icon;

  return (
    <div className="flex items-start gap-3 max-w-4xl mx-auto py-4">
      <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shrink-0 shadow-md animate-pulse">
        <Bot className="w-4 h-4 text-white" />
      </div>

      <div className="glass-panel rounded-2xl rounded-tl-sm p-4 border border-indigo-500/30 flex items-center gap-3">
        <CurrentIcon className="w-4 h-4 text-indigo-400 animate-spin" />
        <span className="text-sm font-medium text-indigo-200 animate-pulse">
          {steps[step].text}
        </span>
      </div>
    </div>
  );
};

export default Loading;
