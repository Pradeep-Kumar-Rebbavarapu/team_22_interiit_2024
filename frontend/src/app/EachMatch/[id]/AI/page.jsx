'use client'

import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Send, Info, Trophy, UserCircle2, ChevronLeft } from "lucide-react"
import Link from "next/link"

export default function Dream11AIChat() {
  const [input, setInput] = useState('')
  const [chatHistory, setChatHistory] = useState([
    {
      id: 1,
      text: "Hi! I'm your Dream11 AI assistant. I can help you create winning teams and understand match statistics.",
      isUser: false,
    },
    {
      id: 2,
      text: "For example, I can help you analyze player performance, suggest captain choices, or explain fantasy points systems.",
      isUser: false,
    },
  ])

  const handleSend = () => {
    if (input.trim()) {
      const newMessage = {
        id: chatHistory.length + 1,
        text: input.trim(),
        isUser: true,
      }
      setChatHistory([...chatHistory, newMessage])
      setInput('')
      // Here you would typically send the message to your AI backend
      // and then add the AI's response to the chat history
    }
  }

  return (
    <div className="flex flex-col h-screen bg-[#1a1c1e] text-white">
      {/* Header (now visible on both mobile and desktop) */}
      <header className="flex items-center gap-2 p-4 border-b border-gray-800">
        <Link href="#" className="flex items-center gap-2 text-white hover:text-gray-300">
          <Button variant="ghost" size="icon" className="text-white hover:bg-gray-800">
            <ChevronLeft className="w-5 h-5" />
            <span className="sr-only">Back to previous page</span>
          </Button>
          <span className="text-sm font-medium">Back to Dream11</span>
        </Link>
      </header>

      {/* Chat Area */}
      <ScrollArea className="flex-1 p-4">
        <div className="max-w-3xl mx-auto space-y-6">
          {chatHistory.map((message) => (
            <div
              key={message.id}
              className={`flex items-start gap-4 ${message.isUser ? 'justify-end' : 'justify-start'}`}
            >
              {!message.isUser && (
                <div className="w-8 h-8 rounded-full bg-[#e53935] flex items-center justify-center flex-shrink-0">
                  <Trophy className="w-5 h-5" />
                </div>
              )}
              <div
                className={`rounded-lg p-4 max-w-[80%] ${
                  message.isUser
                    ? 'bg-[#e53935] text-white'
                    : 'bg-gray-800 text-white'
                }`}
              >
                <p className="text-sm">{message.text}</p>
              </div>
              {message.isUser && (
                <div className="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center flex-shrink-0">
                  <UserCircle2 className="w-5 h-5" />
                </div>
              )}
            </div>
          ))}
        </div>
      </ScrollArea>

      {/* Input Area */}
      <div className="border-t border-gray-800 p-4">
        <div className="max-w-3xl mx-auto flex gap-4">
          <div className="flex-1 relative">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Message Dream11 AI..."
              className="w-full bg-gray-800 border-gray-700 text-white placeholder-gray-400 pr-10"
            />
            <Button
              onClick={handleSend}
              size="icon"
              className="absolute right-2 top-1/2 -translate-y-1/2 bg-transparent hover:bg-gray-700"
            >
              <Send className="w-4 h-4" />
              <span className="sr-only">Send message</span>
            </Button>
          </div>
          <Button size="icon" variant="outline" className="border-gray-700 text-white hover:bg-gray-800">
            <Info className="w-4 h-4" />
            <span className="sr-only">Information</span>
          </Button>
        </div>
        <p className="text-xs text-center mt-2 text-gray-400">
          Dream11 AI may produce inaccurate information. Consider checking important information.
        </p>
      </div>
    </div>
  )
}