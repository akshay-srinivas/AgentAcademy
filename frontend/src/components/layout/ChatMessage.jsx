export default function ChatMessage({ message, isBot }) {
  return (
    <div className={`flex ${isBot ? 'justify-start' : 'justify-end'}`}>
      <div 
        className={`max-w-xs px-4 py-2 rounded-2xl shadow-md ${
          isBot 
            ? 'bg-gray-100 text-gray-700 rounded-bl-none' 
            : 'bg-green-600 text-white rounded-br-none'
        }`}
      >
        {message}
      </div>
    </div>
  );
}