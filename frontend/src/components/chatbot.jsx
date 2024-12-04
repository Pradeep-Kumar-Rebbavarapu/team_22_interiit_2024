'use client'

import React, { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import {
  Send,
  Info,
  Trophy,
  UserCircle2,
  ChevronLeft,
  MessageCircle,
} from "lucide-react"
import AudioBar from '@/components/ui/audio'
import { webSocketConnection } from "@/lib/websockets"
import { TypeAnimation } from 'react-type-animation'
import { getMatchRelatedChats } from "@/api"

const TypingIndicator = () => {
  const [dots, setDots] = useState('.')

  useEffect(() => {
    const interval = setInterval(() => {
      setDots(prev => prev.length >= 3 ? '.' : prev + '.')
    }, 500)

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="flex items-start gap-4 justify-start">
      <div className="w-8 h-8 rounded-full bg-[#e53935] flex items-center justify-center flex-shrink-0">
        <Trophy className="w-5 h-5 text-white" />
      </div>
      <div className="rounded-lg p-4 max-w-[80%] bg-gray-800 text-white">
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
          <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
          <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '600ms' }}></div>
        </div>
      </div>
    </div>
  )
}

export default function Dream11AIChat({ match_id }) {
  const [isOpen, setIsOpen] = useState(false)
  const [input, setInput] = useState("")
  const [chatHistory, setChatHistory] = useState([])
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef(null)

  const addMessage = (message) => {
    setIsTyping(false)
    const aiMessage = {
      id: Date.now().toString(),
      text: message,
      isUser: false,
    }
    setChatHistory((prev) => [...prev, aiMessage])
  }

  webSocketConnection.addMessage = addMessage

  const toggleChat = () => setIsOpen(!isOpen)

  const handleSend = () => {
    if (input.trim()) {
      const text = input.trim()
      const userMessage = {
        id: Date.now().toString(),
        text,
        isUser: true,
      }
      setChatHistory((prev) => [...prev, userMessage])
      setIsTyping(true)
      webSocketConnection.sendMessage(userMessage.text, match_id)
      setInput("")
    }
  }

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [chatHistory, isTyping])

  useEffect(() => {
    const fetchMatchChats = async () => {
      try {
        const matchChats = await getMatchRelatedChats({ match_id: match_id })
        setChatHistory(matchChats.map((chat) => ({
          id: chat.id,
          text: chat.message,
          isUser: chat.is_user,
        })))
      } catch (error) {
        console.error("Error fetching match chats:", error)
      }
    }

    if (isOpen) {
      fetchMatchChats()
    }
  }, [match_id, isOpen])

  if (!isOpen) {
    return (
      <Button
        onClick={toggleChat}
        className="fixed bottom-4 right-4 rounded-full w-14 h-14 bg-[#e53935] hover:bg-[#d32f2f] text-white shadow-lg transition-all duration-300 ease-in-out transform"
        aria-label="Open chat"
      >
        <MessageCircle className="h-6 w-6" />
      </Button>
    )
  }

  return (
    <div className="fixed inset-2 sm:inset-auto sm:bottom-4 sm:right-4 sm:w-96 md:w-[450px] lg:w-[500px] h-[calc(100vh-16px)] sm:h-[600px] flex flex-col bg-[#1a1c1e] text-white rounded-lg shadow-xl overflow-hidden">
      <header className="flex items-center gap-2 p-4 border-b border-gray-800">
        <Button
          variant="ghost"
          size="icon"
          className="text-white hover:bg-gray-800"
          onClick={toggleChat}
          aria-label="Close chat"
        >
          <ChevronLeft className="w-5 h-5" />
        </Button>
        <span className="text-sm font-medium">Dream11 AI Chat</span>
      </header>

      <ScrollArea className="flex-1 p-4">
        <div className="space-y-6">
          {chatHistory.map((message) => (
            <div
              key={message.id}
              className={`flex items-start gap-4 ${message.isUser ? "justify-end" : "justify-start"
                }`}
            >
              {!message.isUser && (
                <div className="w-8 h-8 rounded-full bg-[#e53935] flex items-center justify-center flex-shrink-0">
                  <Trophy className="w-5 h-5 text-white" />
                </div>
              )}
                <div
                    className={`rounded-lg p-4 relative max-w-[80%] ${message.isUser
                    ? "bg-[#e53935] text-white"
                    : "bg-gray-800 text-white"
                    }`}
                >
                <div className="text-sm break-all">
                  {message.text}
                  <AudioBar text={message.text}/>
                </div>
              </div>
              {message.isUser && (
                <div className="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center flex-shrink-0">
                  <UserCircle2 className="w-5 h-5 text-white" />
                </div>
              )}
            </div>
          ))}
          {isTyping && <TypingIndicator />}
          <div ref={messagesEndRef} />
        </div>
      </ScrollArea>

      <div className="border-t border-gray-800 p-4">
        <div className="flex gap-4">
          <div className="flex-1 relative">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && handleSend()}
              placeholder="Message Dream11 AI..."
              className="w-full bg-gray-800 border-gray-700 text-white placeholder-gray-400 pr-10"
            />
            <Button
              onClick={handleSend}
              size="icon"
              className="absolute right-2 top-1/2 -translate-y-1/2 bg-transparent hover:bg-gray-700"
              aria-label="Send message"
            >
              <Send className="w-4 h-4" />
            </Button>
          </div>
          <Button
            size="icon"
            variant="outline"
            className="border-gray-700 text-white hover:bg-gray-800"
            aria-label="Information"
          >
            <Info className="w-4 h-4" />
          </Button>
        </div>
        <p className="text-xs text-center mt-2 text-gray-400">
          Dream11 AI may produce inaccurate information. Consider checking
          important information.
        </p>
      </div>
    </div>
  )
}
