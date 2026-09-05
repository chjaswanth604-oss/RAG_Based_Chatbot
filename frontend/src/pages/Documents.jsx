import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Upload, Trash2, RefreshCw, FileText, CheckCircle, AlertCircle, ArrowLeft, Plus, X, Layers, Clock } from 'lucide-react';
import { documentService } from '../services/api';

const DEPARTMENTS = [
  "General",
  "Computer Science",
  "Electrical Engineering",
  "Mechanical Engineering",
  "Civil Engineering",
  "Electronics"
];

const Documents = () => {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isUploadOpen, setIsUploadOpen] = useState(false);

  // Form State
  const [selectedFile, setSelectedFile] = useState(null);
  const [department, setDepartment] = useState('General');
  const [uploading, setUploading] = useState(false);
  const [uploadStep, setUploadStep] = useState(0);
  const [errorMsg, setErrorMsg] = useState('');

  const fetchDocuments = async () => {
    setLoading(true);
    try {
      const res = await documentService.getDocuments();
      setDocuments(res.data);
    } catch (err) {
      console.error("Failed to fetch documents:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleUploadSubmit = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      setErrorMsg("Please select a PDF, TXT, or DOCX document file.");
      return;
    }

    setErrorMsg('');
    setUploading(true);
    setUploadStep(1); // Uploading & Extracting

    const timer1 = setTimeout(() => setUploadStep(2), 1000); // Creating Chunks
    const timer2 = setTimeout(() => setUploadStep(3), 2000); // Generating Embeddings & ChromaDB

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('department', department);

      await documentService.uploadDocument(formData);
      setUploadStep(4); // Completed

      setTimeout(() => {
        setIsUploadOpen(false);
        setSelectedFile(null);
        setUploading(false);
        setUploadStep(0);
        fetchDocuments();
      }, 1000);
    } catch (err) {
      console.error("Document upload failed:", err);
      setErrorMsg(err.response?.data?.detail || "Document processing failed.");
      setUploading(false);
      setUploadStep(0);
    } finally {
      clearTimeout(timer1);
      clearTimeout(timer2);
    }
  };

  const handleDelete = async (id, docName) => {
    if (!window.confirm(`Are you sure you want to delete '${docName}' from the knowledge base?`)) return;
    try {
      await documentService.deleteDocument(id);
      setDocuments(prev => prev.filter(d => d.id !== id));
    } catch (err) {
      console.error("Delete failed:", err);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 md:p-10">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Top Header Navigation */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-800 pb-6">
          <div>
            <Link to="/admin" className="text-xs text-indigo-400 hover:underline flex items-center gap-1 mb-1">
              <ArrowLeft className="w-3.5 h-3.5" /> Back to Dashboard
            </Link>
            <h1 className="text-2xl md:text-3xl font-extrabold text-white tracking-tight">
              Knowledge Base Management
            </h1>
            <p className="text-sm text-slate-400">
              Upload documents, set departments, and manage vector indexes
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={fetchDocuments}
              className="p-2.5 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 hover:text-white transition-colors"
              title="Refresh List"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            </button>
            <button
              onClick={() => setIsUploadOpen(true)}
              className="flex items-center gap-2 py-2.5 px-4 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl font-semibold text-sm transition-all shadow-lg shadow-indigo-600/30 glow-primary"
            >
              <Plus className="w-4 h-4" />
              Upload New Document
            </button>
          </div>
        </div>

        {/* Upload Modal Drawer */}
        {isUploadOpen && (
          <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="glass-panel max-w-lg w-full rounded-2xl p-6 border border-slate-800 shadow-2xl relative">
              <button
                onClick={() => setIsUploadOpen(false)}
                disabled={uploading}
                className="absolute top-4 right-4 text-slate-400 hover:text-white"
              >
                <X className="w-5 h-5" />
              </button>

              <div className="flex items-center gap-3 mb-4">
                <div className="p-3 rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                  <Upload className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-bold text-lg text-white">Upload College Document</h3>
                  <p className="text-xs text-slate-400">Supported formats: PDF, DOCX, TXT</p>
                </div>
              </div>

              {errorMsg && (
                <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 flex items-center gap-2 text-rose-300 text-xs mb-4">
                  <AlertCircle className="w-4 h-4 shrink-0" />
                  <span>{errorMsg}</span>
                </div>
              )}

              <form onSubmit={handleUploadSubmit} className="space-y-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                    Select Document File
                  </label>
                  <input
                    type="file"
                    accept=".pdf,.txt,.docx"
                    required
                    onChange={(e) => setSelectedFile(e.target.files[0])}
                    className="w-full text-xs text-slate-300 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-indigo-600 file:text-white hover:file:bg-indigo-500 cursor-pointer bg-slate-900 border border-slate-800 rounded-xl p-1"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                    Target Department
                  </label>
                  <select
                    value={department}
                    onChange={(e) => setDepartment(e.target.value)}
                    className="w-full bg-slate-900 border border-slate-800 text-sm text-slate-200 rounded-xl px-3.5 py-2.5 focus:outline-none focus:border-indigo-500 transition-colors"
                  >
                    {DEPARTMENTS.map((dept) => (
                      <option key={dept} value={dept}>{dept}</option>
                    ))}
                  </select>
                </div>

                {/* Processing status steps indicator */}
                {uploading && (
                  <div className="p-3.5 rounded-xl bg-indigo-950/40 border border-indigo-500/30 text-xs space-y-2">
                    <div className="flex items-center gap-2 text-indigo-300 font-medium">
                      <Clock className="w-4 h-4 animate-spin text-indigo-400" />
                      {uploadStep === 1 && "Uploading document & extracting text page-by-page..."}
                      {uploadStep === 2 && "Splitting text into semantic chunks (~500 words)..."}
                      {uploadStep === 3 && "Generating Sentence Transformer embeddings & indexing in ChromaDB..."}
                      {uploadStep === 4 && "Document processing completed successfully!"}
                    </div>
                  </div>
                )}

                <div className="flex items-center justify-end gap-3 pt-2">
                  <button
                    type="button"
                    onClick={() => setIsUploadOpen(false)}
                    disabled={uploading}
                    className="py-2.5 px-4 rounded-xl border border-slate-800 text-xs font-semibold text-slate-300 hover:bg-slate-900"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={uploading}
                    className="py-2.5 px-5 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-xs font-semibold text-white shadow-lg glow-primary"
                  >
                    {uploading ? 'Processing...' : 'Upload & Process'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Documents Table */}
        <div className="glass-panel rounded-2xl border border-slate-800 overflow-hidden shadow-2xl">
          {loading ? (
            <div className="p-12 text-center text-slate-500 text-sm animate-pulse">
              Loading knowledge base documents...
            </div>
          ) : documents.length === 0 ? (
            <div className="p-12 text-center text-slate-500 space-y-3">
              <FileText className="w-10 h-10 mx-auto text-slate-600" />
              <p className="text-base font-semibold text-slate-300">No documents found in knowledge base</p>
              <p className="text-xs text-slate-500">Upload sample PDFs to populate the vector search database.</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm text-slate-300">
                <thead className="bg-slate-900/90 text-xs uppercase font-semibold text-slate-400 border-b border-slate-800">
                  <tr>
                    <th className="px-6 py-4">Document Name</th>
                    <th className="px-6 py-4">Department</th>
                    <th className="px-6 py-4">Pages / Chunks</th>
                    <th className="px-6 py-4">Upload Date</th>
                    <th className="px-6 py-4">Status</th>
                    <th className="px-6 py-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {documents.map((doc) => (
                    <tr key={doc.id} className="hover:bg-slate-900/40 transition-colors">
                      <td className="px-6 py-4 font-medium text-slate-100 flex items-center gap-3">
                        <FileText className="w-4 h-4 text-indigo-400 shrink-0" />
                        <span className="truncate max-w-xs">{doc.document_name}</span>
                      </td>
                      <td className="px-6 py-4">
                        <span className="px-2.5 py-1 rounded-md bg-slate-800 text-slate-300 text-xs font-medium border border-slate-700">
                          {doc.department}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-xs text-slate-400">
                        {doc.page_count} Pages ({doc.chunks_count} Chunks)
                      </td>
                      <td className="px-6 py-4 text-xs text-slate-400">
                        {doc.upload_date ? new Date(doc.upload_date).toLocaleDateString() : 'N/A'}
                      </td>
                      <td className="px-6 py-4">
                        <span className={`px-2.5 py-1 rounded-full text-xs font-semibold border flex items-center gap-1.5 w-fit ${
                          doc.status === 'Processed'
                            ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                            : doc.status === 'Processing'
                            ? 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                            : 'bg-rose-500/10 text-rose-400 border-rose-500/30'
                        }`}>
                          {doc.status === 'Processed' && <CheckCircle className="w-3.5 h-3.5" />}
                          {doc.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-right">
                        <button
                          onClick={() => handleDelete(doc.id, doc.document_name)}
                          className="p-1.5 rounded-lg hover:bg-rose-500/10 text-slate-400 hover:text-rose-400 transition-colors"
                          title="Delete Document"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Documents;
