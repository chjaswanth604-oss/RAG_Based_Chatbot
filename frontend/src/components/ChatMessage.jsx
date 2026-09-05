import React, { useState } from 'react';
import { Bot, User, ThumbsUp, ThumbsDown, Layers, Check } from 'lucide-react';
import SourceCard from './SourceCard';
import { feedbackService } from '../services/api';

const ChatMessage = ({ message, chatId }) => {
  const { question, answer, sources, relevance_score, created_at } = message;
  const [feedback, setFeedback] = useState(null); // 'thumbs_up' | 'thumbs_down' | null
  const [feedbackSent, setFeedbackSent] = useState(false);

  const handleFeedback = async (type) => {
    if (feedbackSent) return;
    setFeedback(type);
    try {
      await feedbackService.submitFeedback({
        chat_id: chatId || 'default',
        question: question,
        answer: answer,
        feedback: type
      });
      setFeedbackSent(true);
    } catch (err) {
      console.error("Feedback error:", err);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto py-4">
      {/* User Message Bubble */}
      <div className="flex items-start justify-end gap-3">
        <div className="bg-indigo-600/90 text-white rounded-2xl rounded-tr-sm px-5 py-3 max-w-[80%] shadow-lg">
          <p className="text-sm md:text-base leading-relaxed whitespace-pre-wrap">{question}</p>
        </div>
        <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center shrink-0">
          <User className="w-4 h-4 text-indigo-400" />
        </div>
      </div>

      {/* AI Assistant Message Bubble */}
      <div className="flex items-start gap-3">
        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shrink-0 shadow-md glow-primary">
          <Bot className="w-4 h-4 text-white" />
        </div>

        <div className="space-y-4 max-w-[88%]">
          {/* Main Answer Card */}
          <div className="glass-panel rounded-2xl rounded-tl-sm p-5 shadow-xl border border-slate-800 text-slate-100">
            <p className="text-sm md:text-base leading-relaxed whitespace-pre-wrap">{answer}</p>

            {/* Source Citations Section */}
            {sources && sources.length > 0 && (
              <div className="mt-5 pt-4 border-t border-slate-800/80">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2 text-xs font-semibold text-indigo-300 uppercase tracking-wider">
                    <Layers className="w-3.5 h-3.5" />
                    Source References ({sources.length})
                  </div>
                  {relevance_score > 0 && (
                    <span className="text-xs text-slate-400">
                      Max Relevance: <strong className="text-emerald-400">{Math.round(relevance_score * 100)}%</strong>
                    </span>
                  )}
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                  {sources.map((src, index) => (
                    <SourceCard key={index} source={src} />
                  ))}
                </div>
              </div>
            )}

            {/* Feedback Footer */}
            <div className="mt-4 pt-3 flex items-center justify-between text-xs text-slate-400 border-t border-slate-800/40">
              <span>Was this response helpful?</span>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => handleFeedback('thumbs_up')}
                  disabled={feedbackSent}
                  className={`p-1.5 rounded-lg border transition-all ${
                    feedback === 'thumbs_up'
                      ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/50'
                      : 'border-slate-800 hover:border-slate-700 hover:text-slate-200'
                  }`}
                  title="Helpful"
                >
                  <ThumbsUp className="w-3.5 h-3.5" />
                </button>
                <button
                  onClick={() => handleFeedback('thumbs_down')}
                  disabled={feedbackSent}
                  className={`p-1.5 rounded-lg border transition-all ${
                    feedback === 'thumbs_down'
                      ? 'bg-rose-500/20 text-rose-400 border-rose-500/50'
                      : 'border-slate-800 hover:border-slate-700 hover:text-slate-200'
                  }`}
                  title="Not helpful"
                >
                  <ThumbsDown className="w-3.5 h-3.5" />
                </button>
                {feedbackSent && (
                  <span className="text-[11px] text-emerald-400 flex items-center gap-1 ml-1">
                    <Check className="w-3 h-3" /> Thank you!
                  </span>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;
