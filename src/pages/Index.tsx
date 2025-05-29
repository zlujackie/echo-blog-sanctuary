
import { useState } from "react";
import { Link } from "react-router-dom";
import { Calendar, Clock, User } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

// 模拟文章数据
const mockPosts = [
  {
    id: 1,
    title: "探索现代前端开发的最新趋势",
    excerpt: "从React到Vue，从TypeScript到WebAssembly，现代前端开发正在经历前所未有的变革。本文将深入探讨这些技术的发展方向。",
    author: "张三",
    publishDate: "2024-05-29",
    readTime: "5分钟",
    category: "技术",
    image: "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=800&h=400&fit=crop",
  },
  {
    id: 2,
    title: "人工智能时代的思考",
    excerpt: "AI正在改变我们的工作和生活方式。作为开发者，我们应该如何适应这个变化，并在其中找到自己的位置？",
    author: "张三",
    publishDate: "2024-05-28",
    readTime: "8分钟",
    category: "思考",
    image: "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&h=400&fit=crop",
  },
  {
    id: 3,
    title: "代码之美：编程中的艺术哲学",
    excerpt: "优雅的代码不仅仅是功能的实现，更是一种艺术表达。本文探讨如何写出既高效又美观的代码。",
    author: "张三",
    publishDate: "2024-05-27",
    readTime: "6分钟",
    category: "编程",
    image: "https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=800&h=400&fit=crop",
  }
];

const Index = () => {
  const [selectedCategory, setSelectedCategory] = useState("全部");
  const categories = ["全部", "技术", "思考", "编程", "生活"];

  const filteredPosts = selectedCategory === "全部" 
    ? mockPosts 
    : mockPosts.filter(post => post.category === selectedCategory);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <Header />
      
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-white to-blue-100 bg-clip-text text-transparent">
            我的技术博客
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-blue-100 max-w-3xl mx-auto">
            分享技术见解，记录成长历程，探索编程世界的无限可能
          </p>
          <div className="flex justify-center space-x-4">
            <Badge variant="secondary" className="px-4 py-2 text-lg">
              前端开发
            </Badge>
            <Badge variant="secondary" className="px-4 py-2 text-lg">
              技术思考
            </Badge>
            <Badge variant="secondary" className="px-4 py-2 text-lg">
              编程分享
            </Badge>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-12">
        {/* Category Filter */}
        <div className="flex flex-wrap gap-2 mb-8 justify-center">
          {categories.map(category => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`px-4 py-2 rounded-full transition-all duration-300 ${
                selectedCategory === category
                  ? "bg-blue-600 text-white shadow-lg"
                  : "bg-white text-gray-600 hover:bg-blue-50 border"
              }`}
            >
              {category}
            </button>
          ))}
        </div>

        {/* Articles Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {filteredPosts.map(post => (
            <Link key={post.id} to={`/post/${post.id}`}>
              <Card className="h-full hover:shadow-xl transition-all duration-300 transform hover:-translate-y-2 group overflow-hidden">
                <div className="relative overflow-hidden">
                  <img 
                    src={post.image} 
                    alt={post.title}
                    className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                  <div className="absolute top-4 left-4">
                    <Badge className="bg-white/90 text-gray-800">
                      {post.category}
                    </Badge>
                  </div>
                </div>
                <CardHeader className="pb-3">
                  <CardTitle className="text-xl group-hover:text-blue-600 transition-colors line-clamp-2">
                    {post.title}
                  </CardTitle>
                </CardHeader>
                <CardContent className="pt-0">
                  <p className="text-gray-600 mb-4 line-clamp-3">
                    {post.excerpt}
                  </p>
                  <div className="flex items-center justify-between text-sm text-gray-500">
                    <div className="flex items-center space-x-4">
                      <div className="flex items-center space-x-1">
                        <User size={14} />
                        <span>{post.author}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Calendar size={14} />
                        <span>{post.publishDate}</span>
                      </div>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Clock size={14} />
                      <span>{post.readTime}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Index;
