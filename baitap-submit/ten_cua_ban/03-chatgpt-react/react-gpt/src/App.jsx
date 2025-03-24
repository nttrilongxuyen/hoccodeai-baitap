import { useState } from 'react'
import reactLogo from './assets/react.svg'
import Together from 'together-ai'


const client = new Together({
  apiKey: import.meta.env.VITE_TOGETHER_KEY
});

function App() {
  const [message, setMessage] = useState("")
  const [messages, setMessages] = useState([])
  

  const submitMessage = async (e) => {
    e.preventDefault()
    setMessage('')
    const inputMsg = [
      ...messages,
      {
        role: 'user',
        content: message
      }
    ]

    setMessages(
      [
        ...messages,
        {
          role: 'user',
          content: message
        },
        {
          role: 'assistant',
          content: "Loading..."
        }
      ]
    )

    const chatCompletion = await client.chat.completions.create({
      messages: inputMsg,
      model: 'meta-llama/Llama-3.3-70B-Instruct-Turbo-Free',
    });

    const response = await chatCompletion.choices[0].message.content
   
    setMessages(
      [
        ...messages,
        {
          role: 'user',
          content: message
        },
        {
          role: 'assistant',
          content: response
        }
      ]
    )
  }

  return (
    <div className="bg-gray-100 h-screen flex flex-col">
      <div className="container mx-auto p-4 flex flex-col h-full max-w-2xl">
        <h1 className="text-2xl font-bold mb-4">ChatUI với React + OpenAI</h1>
        <form className="flex">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Tin nhắn của bạn..."
            className="flex-grow p-2 rounded-l border border-gray-300"
          />
          <button
            type="submit"
            className="bg-blue-500 text-white px-4 py-2 rounded-r hover:bg-blue-600"
            onClick={(e) => { submitMessage(e) }}
          >
            Gửi tin nhắn
          </button>
        </form>

        <div className="flex-grow overflow-y-auto mt-4 bg-white rounded shadow p-4">
          {messages.map((msg) =>
             (<div className={`mb-2  ${msg.role ==="assistant" ? 'text-right' : ''}`}>
              <p className="text-gray-600 text-sm">{msg.role}</p>
              <p className={`p-2 rounded-lg inline-block ${msg.role ==="assistant" ? 'bg-green-100 ' : 'bg-blue-100 '}`}>
                {msg.content}
              </p>
            </div>)
          )}
        </div>
      </div>
    </div>
  );
}

export default App
