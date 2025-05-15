import { X, Send } from "lucide-react";
import ChatMessage from "../layout/ChatMessage";

export default function Chatbot({ setShowChatbot }) {
  return (
    <div className="w-80 bg-white border-l border-gray-200 flex flex-col">
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <h3 className="font-semibold">AI Learning Assistant</h3>
          <button onClick={() => setShowChatbot(false)} className="text-gray-500 hover:text-gray-700">
            <X size={18} />
          </button>
        </div>
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        <ChatMessage 
          message="Hi Alex! Need help with anything in your training today?" 
          isBot={true} 
        />
        <ChatMessage 
          message="I'm working on the advanced troubleshooting scenario, but I'm stuck on the network diagnostics part" 
          isBot={false} 
        />
        <ChatMessage 
          message="I can help with that! For network diagnostics, remember to follow these steps: 1) Verify connectivity 2) Check DNS resolution 3) Test latency. Would you like me to explain any of these in more detail?" 
          isBot={true} 
        />
      </div>
      <div className="p-4 border-t border-gray-200">
        <div className="flex items-center">
          <input
            type="text"
            placeholder="Ask anything..."
            className="flex-1 py-2 px-3 border border-gray-300 rounded-l-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          />
          <button className="bg-indigo-600 text-white p-2 rounded-r-lg">
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}