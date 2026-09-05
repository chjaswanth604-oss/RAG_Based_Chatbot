import React, { useState, useEffect, useRef } from 'react';
import { Send, Menu, Sparkles, Filter, Bot, Trash2 } from 'lucide-react';
import Sidebar from '../components/Sidebar';
import ChatMessage from '../components/ChatMessage';
import Loading from '../components/Loading';
import SuggestedQuestions from '../components/SuggestedQuestions';
import { chatService } from '../services/api';

const DEPARTMENTS = [
  "All",
  "General",
  "Computer Science",
  "Electrical Engineering",
  "Mechanical Engineering",
  "Civil Engineering",
  "Electronics"
];

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [inputQuery, setInputQuery] = useState('');
  const [currentChatId, setCurrentChatId] = useState(null);
  const [deptFilter, setDeptFilter] = useState('All');
  const [loading, setLoading] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSelectChat = async (chatId) => {
    setCurrentChatId(chatId);
    setLoading(true);
    try {
      const res = await chatService.getChatDetail(chatId);
      setMessages(res.data.messages || []);
    } catch (err) {
      console.error("Failed to fetch chat details:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleNewChat = () => {
    setCurrentChatId(null);
    setMessages([]);
    setInputQuery('');
  };

  const handleSend = async (queryText) => {
    const text = queryText || inputQuery;
    if (!text.trim() || loading) return;

    setInputQuery('');
    setLoading(true);

    try {
      const payload = {
        question: text.trim(),
        chat_id: currentChatId,
        department_filter: deptFilter !== 'All' ? deptFilter : null,
      };

      const res = await chatService.sendMessage(payload);
      const newMsg = res.data;

      if (!currentChatId) {
        setCurrentChatId(newMsg.chat_id);
      }

      setMessages((prev) => [...prev, newMsg]);
    } catch (err) {
      console.error("Chat send error:", err);
      // Append fallback error message
      setMessages((prev) => [
        ...prev,
        {
          question: text,
          answer: "Unable to process your question at this moment. Please check backend connection.",
          sources: [],
          relevance_score: 0.0,
          created_at: new Date().toISOString(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 overflow-hidden">
      {/* Collapsible Sidebar */}
      <Sidebar
        currentChatId={currentChatId}
        onSelectChat={handleSelectChat}
        onNewChat={handleNewChat}
        isOpen={isSidebarOpen}
        setIsOpen={setIsSidebarOpen}
      />

      {/* Main Chat Content Area */}
      <div className="flex-1 flex flex-col h-full relative overflow-hidden bg-slate-950">
        {/* Background glow graphics */}
        <div className="absolute top-0 right-1/4 w-96 h-96 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none" />

        {/* Top Header Navbar */}
        <header className="h-16 border-b border-slate-800/80 px-4 md:px-6 flex items-center justify-between bg-slate-900/60 backdrop-blur-md z-10">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
              className="lg:hidden p-2 rounded-lg hover:bg-slate-800 text-slate-400"
            >
              <Menu className="w-5 h-5" />
            </button>
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
              <h2 className="font-semibold text-sm md:text-base text-slate-200">
                College AI Knowledge Assistant
              </h2>
            </div>
          </div>

          {/* Department Filter Dropdown */}
          <div className="flex items-center gap-2">
            <Filter className="w-4 h-4 text-slate-400 hidden sm:block" />
            <select
              value={deptFilter}
              onChange={(e) => setDeptFilter(e.target.value)}
              className="bg-slate-900 border border-slate-800 text-xs text-slate-300 rounded-lg px-3 py-1.5 focus:outline-none focus:border-indigo-500 transition-colors"
            >
              {DEPARTMENTS.map((dept) => (
                <option key={dept} value={dept}>
                  {dept === 'All' ? 'All Departments' : dept}
                </option>
              ))}
            </select>
          </div>
        </header>

        {/* Chat Scroll Window */}
        <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-4">
          {messages.length === 0 ? (
            <div className="max-w-4xl mx-auto py-8">
              {/* Hero Banner */}
              <div className="text-center py-6">
                <div className="inline-flex p-3 rounded-2xl bg-gradient-to-tr from-indigo-500/20 to-purple-500/20 border border-indigo-500/30 mb-4 shadow-xl">
                  <Bot className="w-10 h-10 text-indigo-400" />
                </div>
                <h1 className="text-2xl md:text-3xl font-extrabold text-white tracking-tight mb-2">
                  What would you like to know about college?
                </h1>
                <p className="text-sm text-slate-400 max-w-xl mx-auto">
                  Ask questions about academic regulations, fee structure, hostel rules, library timings, placement statistics, or departmental standards.
                </p>
              </div>

              {/* Suggested Questions Cards */}
              <SuggestedQuestions onSelectQuestion={(q) => handleSend(q)} />
            </div>
          ) : (
            messages.map((msg, index) => (
              <ChatMessage key={index} message={msg} chatId={currentChatId} />
            ))
          )}

          {loading && <Loading />}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Bar Footer */}
        <div className="p-4 md:p-6 bg-slate-900/80 border-t border-slate-800/80 backdrop-blur-md z-10">
          <div className="max-w-4xl mx-auto relative">
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSend();
              }}
              className="flex items-center gap-2 bg-slate-900 border border-slate-800 focus-within:border-indigo-500/80 rounded-2xl p-2 transition-all duration-200 shadow-xl"
            >
              <input
                type="text"
                value={inputQuery}
                onChange={(e) => setInputQuery(e.target.value)}
                placeholder="Ask about attendance rules, hostel timings, fees, scholarships..."
                className="flex-1 bg-transparent px-4 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none"
              />
              <button
                type="submit"
                disabled={!inputQuery.trim() || loading}
                className="p-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 text-white transition-all duration-200 shadow-lg glow-primary"
              >
                <Send className="w-4 h-4" />
              </button>
            </form>
            <p className="text-[11px] text-center text-slate-500 mt-2">
              Answers are generated strictly from uploaded college documents using semantic vector RAG.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chat;
