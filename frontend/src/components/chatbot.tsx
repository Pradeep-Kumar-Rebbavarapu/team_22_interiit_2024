"use client";

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Send,
  Info,
  Trophy,
  UserCircle2,
  ChevronLeft,
  MessageCircle,
} from "lucide-react";
import { webSocketConnection } from "@/lib/websockets";

export default function Dream11AIChat() {
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState("");
  const [chatHistory, setChatHistory] = useState<string[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const toggleChat = () => setIsOpen(!isOpen);

  const handleSend = () => {
    if (input.trim()) {
      const text = input.trim();
      setChatHistory([...chatHistory, text]);
      setInput("");
      // Simulate AI response
      setTimeout(() => {
        const text =
          "Thank you for your message. I'm processing your request and will provide assistance shortly.";
        setChatHistory((prev) => [...prev, text]);
      }, 1000);
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatHistory]);

  if (!isOpen) {
    return (
      <Button
        onClick={toggleChat}
        className="fixed bottom-4 right-4 rounded-full w-14 h-14 bg-[#e53935] hover:bg-[#d32f2f] text-white shadow-lg transition-all duration-300 ease-in-out transform"
      >
        <MessageCircle className="h-6 w-6" />
      </Button>
    );
  }

  return (
    <div className="fixed bottom-4 right-4 w-full max-w-[90vw] sm:max-w-md md:max-w-lg lg:max-w-xl xl:max-w-2xl h-[700px] flex flex-col bg-[#1a1c1e] text-white rounded-lg shadow-xl overflow-hidden">
      {/* Header */}
      <header className="flex items-center gap-2 p-4 border-b border-gray-800">
        <Button
          variant="ghost"
          size="icon"
          className="text-white hover:bg-gray-800"
          onClick={toggleChat}
        >
          <ChevronLeft className="w-5 h-5" />
          <span className="sr-only">Close chat</span>
        </Button>
        <span className="text-sm font-medium">Dream11 AI Chat</span>
      </header>

      {/* Chat Area */}
      <ScrollArea className="flex-1 p-4">
        <div className="space-y-6">
          {chatHistory.map((message) => (
            <div
              key={message.id}
              className={`flex items-start gap-4 ${
                message.isUser ? "justify-end" : "justify-start"
              }`}
            >
              {!message.isUser && (
                <div className="w-8 h-8 rounded-full bg-[#e53935] flex items-center justify-center flex-shrink-0">
                  <Trophy className="w-5 h-5" />
                </div>
              )}
              <div
                className={`rounded-lg p-4 max-w-[80%] ${
                  message.isUser
                    ? "bg-[#e53935] text-white"
                    : "bg-gray-800 text-white"
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
          <div ref={messagesEndRef} />
        </div>
      </ScrollArea>

      {/* Input Area */}
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
            >
              <Send className="w-4 h-4" />
              <span className="sr-only">Send message</span>
            </Button>
          </div>
          <Button
            size="icon"
            variant="outline"
            className="border-gray-700 text-white hover:bg-gray-800"
          >
            <Info className="w-4 h-4" />
            <span className="sr-only">Information</span>
          </Button>
        </div>
        <p className="text-xs text-center mt-2 text-gray-400">
          Dream11 AI may produce inaccurate information. Consider checking
          important information.
        </p>
      </div>
    </div>
  );
}
