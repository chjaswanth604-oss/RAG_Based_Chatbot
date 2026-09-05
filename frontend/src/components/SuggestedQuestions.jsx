import React from 'react';
import { Sparkles, ArrowUpRight } from 'lucide-react';

const SUGGESTIONS = [
  "What is the minimum attendance requirement?",
  "What are the hostel timings?",
  "What is the fee for the course?",
  "What scholarships are available?",
  "How can I apply for placements?",
  "What are the library timings?",
  "What are the electrical engineering lab requirements?",
  "When are the semester examinations?"
];

const SuggestedQuestions = ({ onSelectQuestion }) => {
  return (
    <div className="max-w-4xl mx-auto my-8 p-6 glass-panel rounded-2xl border border-indigo-500/20 glow-primary">
      <div className="flex items-center gap-2 mb-4">
        <Sparkles className="w-5 h-5 text-indigo-400" />
        <h3 className="text-base font-semibold text-slate-200">
          Suggested Questions
        </h3>
      </div>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {SUGGESTIONS.map((q, idx) => (
          <button
            key={idx}
            onClick={() => onSelectQuestion(q)}
            className="flex items-center justify-between p-3.5 rounded-xl bg-slate-900/60 hover:bg-indigo-600/20 border border-slate-800 hover:border-indigo-500/50 text-slate-300 hover:text-white text-left text-sm transition-all duration-200 group"
          >
            <span className="truncate pr-2">{q}</span>
            <ArrowUpRight className="w-4 h-4 text-slate-500 group-hover:text-indigo-400 shrink-0 transition-colors" />
          </button>
        ))}
      </div>
    </div>
  );
};

export default SuggestedQuestions;
