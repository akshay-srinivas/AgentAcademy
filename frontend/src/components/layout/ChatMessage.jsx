export default function ChatMessage({ message, isBot }) {
  return (
    <div className={`flex ${isBot ? 'justify-start' : 'justify-end'}`}>
      <div className={`max-w-xs px-4 py-2 rounded-lg ${
        isBot ? 'bg-gray-100 text-gray-800' : 'bg-indigo-600 text-white'
      }`}>
        {message}
      </div>
    </div>
  );
}