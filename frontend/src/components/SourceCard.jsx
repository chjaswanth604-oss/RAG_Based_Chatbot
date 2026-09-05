import React from 'react';
import { FileText, Bookmark, CheckCircle } from 'lucide-react';

const SourceCard = ({ source }) => {
  const { document, page, score, department } = source;
  const scorePercent = Math.round(score * 100);

  // Badge color depending on score
  const getBadgeColor = (pct) => {
    if (pct >= 75) return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
    if (pct >= 50) return 'bg-indigo-500/10 text-indigo-400 border-indigo-500/30';
    return 'bg-amber-500/10 text-amber-400 border-amber-500/30';
  };

  return (
    <div className="glass-card rounded-xl p-3.5 border border-slate-800 hover:border-indigo-500/40 transition-all duration-200 group">
      <div className="flex items-start justify-between gap-2 mb-2">
        <div className="flex items-center gap-2 min-w-0">
          <div className="p-2 rounded-lg bg-indigo-500/10 text-indigo-400 group-hover:bg-indigo-500/20 transition-colors">
            <FileText className="w-4 h-4 shrink-0" />
          </div>
          <span className="font-medium text-sm text-slate-200 truncate" title={document}>
            {document}
          </span>
        </div>
        <span className={`text-xs px-2 py-0.5 rounded-full border font-medium whitespace-nowrap ${getBadgeColor(scorePercent)}`}>
          {scorePercent}% Match
        </span>
      </div>

      <div className="flex items-center justify-between text-xs text-slate-400 pt-1 border-t border-slate-800/60">
        <span className="flex items-center gap-1">
          <Bookmark className="w-3 h-3 text-slate-500" />
          Page {page}
        </span>
        {department && (
          <span className="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px]">
            {department}
          </span>
        )}
      </div>
    </div>
  );
};

export default SourceCard;
