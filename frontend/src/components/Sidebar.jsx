import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, MessageSquare, Trash2, LogOut, ShieldAlert, BookOpen, User, ChevronRight } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { chatService } from '../services/api';

const Sidebar = ({ currentChatId, onSelectChat, onNewChat, isOpen, setIsOpen }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchHistory = async () => {
    try {
      const res = await chatService.getHistory();
      setHistory(res.data);
    } catch (err) {
      console.error("Failed to load chat history:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, [currentChatId]);

  const handleDeleteChat = async (e, id) => {
    e.stopPropagation();
    try {
      await chatService.deleteChat(id);
      setHistory(prev => prev.filter(item => item.id !== id));
      if (currentChatId === id) {
        onNewChat();
      }
    } catch (err) {
      console.error("Failed to delete chat:", err);
    }
  };

  return (
    <aside
      className={`fixed lg:static inset-y-0 left-0 z-40 w-72 bg-slate-900/95 border-r border-slate-800 flex flex-col transition-transform duration-300 ${
        isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
      }`}
    >
      {/* Header & Logo */}
      <div className="p-4 border-b border-slate-800/80 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-600 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/20">
            <BookOpen className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="font-bold text-sm text-slate-100 tracking-tight">Campus AI Assistant</h1>
            <p className="text-[11px] text-indigo-400 font-medium">RAG Document System</p>
          </div>
        </div>
      </div>

      {/* New Chat Button */}
      <div className="p-4">
        <button
          onClick={() => {
            onNewChat();
            if (setIsOpen) setIsOpen(false);
          }}
          className="w-full flex items-center justify-center gap-2 py-2.5 px-4 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl font-medium text-sm transition-all duration-200 shadow-lg shadow-indigo-600/25 glow-primary"
        >
          <Plus className="w-4 h-4" />
          <span>New Conversation</span>
        </button>
      </div>

      {/* Navigation Links (Admin Panel if admin) */}
      {user?.role === 'admin' && (
        <div className="px-4 mb-2">
          <button
            onClick={() => navigate('/admin')}
            className="w-full flex items-center justify-between p-2.5 rounded-xl bg-purple-950/40 border border-purple-500/30 text-purple-300 hover:bg-purple-900/40 text-xs font-semibold transition-colors"
          >
            <span className="flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-purple-400" />
              Admin Dashboard
            </span>
            <ChevronRight className="w-3.5 h-3.5" />
          </button>
        </div>
      )}

      {/* Chat History List */}
      <div className="flex-1 overflow-y-auto px-3 py-2 space-y-1">
        <h2 className="px-3 text-[11px] font-semibold text-slate-500 uppercase tracking-wider mb-2">
          Recent Conversations
        </h2>

        {loading ? (
          <div className="px-3 py-4 text-xs text-slate-500 animate-pulse">Loading history...</div>
        ) : history.length === 0 ? (
          <div className="px-3 py-4 text-xs text-slate-500 italic">No previous chats</div>
        ) : (
          history.map((chat) => (
            <div
              key={chat.id}
              onClick={() => {
                onSelectChat(chat.id);
                if (setIsOpen) setIsOpen(false);
              }}
              className={`group flex items-center justify-between p-2.5 rounded-xl text-xs cursor-pointer transition-all duration-150 ${
                currentChatId === chat.id
                  ? 'bg-slate-800/90 text-indigo-300 font-medium border border-indigo-500/30'
                  : 'text-slate-400 hover:bg-slate-800/40 hover:text-slate-200'
              }`}
            >
              <div className="flex items-center gap-2.5 min-w-0 pr-2">
                <MessageSquare className="w-3.5 h-3.5 shrink-0 text-slate-500 group-hover:text-indigo-400" />
                <span className="truncate">{chat.title}</span>
              </div>
              <button
                onClick={(e) => handleDeleteChat(e, chat.id)}
                className="opacity-0 group-hover:opacity-100 p-1 hover:text-rose-400 text-slate-500 transition-opacity"
                title="Delete Chat"
              >
                <Trash2 className="w-3.5 h-3.5" />
              </button>
            </div>
          ))
        )}
      </div>

      {/* User Profile & Logout Footer */}
      <div className="p-4 border-t border-slate-800/80 bg-slate-900/60">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2.5 min-w-0">
            <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center shrink-0">
              <User className="w-4 h-4 text-indigo-400" />
            </div>
            <div className="min-w-0">
              <p className="text-xs font-semibold text-slate-200 truncate">{user?.name || 'Student'}</p>
              <p className="text-[10px] text-slate-400 capitalize">{user?.role || 'student'}</p>
            </div>
          </div>

          <button
            onClick={logout}
            className="p-2 rounded-lg hover:bg-rose-500/10 text-slate-400 hover:text-rose-400 transition-colors"
            title="Logout"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
