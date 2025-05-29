
import { useParams, Link } from "react-router-dom";
import { Calendar, Clock, User, ArrowLeft } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

// 模拟文章详情数据
const mockPost = {
  id: 1,
  title: "探索现代前端开发的最新趋势",
  content: `
    <h2>引言</h2>
    <p>现代前端开发正在经历前所未有的变革。从React到Vue，从TypeScript到WebAssembly，新技术层出不穷，为开发者提供了更多的选择和可能性。</p>
    
    <h2>React的持续演进</h2>
    <p>React作为前端开发的主流框架之一，持续在性能优化和开发体验方面进行改进。React 18引入了并发特性，使得应用能够更好地处理复杂的用户交互。</p>
    
    <h2>TypeScript的普及</h2>
    <p>TypeScript已经成为现代前端开发的标配。它不仅提供了类型安全，还大大提升了代码的可维护性和开发效率。越来越多的项目选择使用TypeScript作为开发语言。</p>
    
    <h2>构建工具的革新</h2>
    <p>Vite、ESBuild等新一代构建工具以其极快的构建速度赢得了开发者的青睐。这些工具利用现代浏览器的ES模块支持，实现了近乎即时的热更新。</p>
    
    <h2>总结</h2>
    <p>前端技术的发展速度令人惊叹，但核心始终是为用户提供更好的体验。作为开发者，我们需要保持学习的热情，同时也要有选择性地采用新技术。</p>
  `,
  author: "张三",
  publishDate: "2024-05-29",
  readTime: "5分钟",
  category: "技术",
  image: "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=1200&h=600&fit=crop",
};

const BlogPost = () => {
  const { id } = useParams();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Back Button */}
          <Link to="/">
            <Button variant="ghost" className="mb-6 hover:bg-blue-50">
              <ArrowLeft className="mr-2 h-4 w-4" />
              返回文章列表
            </Button>
          </Link>

          {/* Article Header */}
          <article className="bg-white rounded-lg shadow-lg overflow-hidden">
            <div className="relative">
              <img 
                src={mockPost.image} 
                alt={mockPost.title}
                className="w-full h-64 md:h-96 object-cover"
              />
              <div className="absolute inset-0 bg-black bg-opacity-40 flex items-end">
                <div className="p-8 text-white">
                  <Badge className="mb-4 bg-white/20 text-white border-white/30">
                    {mockPost.category}
                  </Badge>
                  <h1 className="text-3xl md:text-5xl font-bold mb-4">
                    {mockPost.title}
                  </h1>
                  <div className="flex items-center space-x-6 text-blue-100">
                    <div className="flex items-center space-x-2">
                      <User size={16} />
                      <span>{mockPost.author}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Calendar size={16} />
                      <span>{mockPost.publishDate}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Clock size={16} />
                      <span>{mockPost.readTime}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Article Content */}
            <div className="p-8 md:p-12">
              <div 
                className="prose prose-lg max-w-none prose-headings:text-gray-900 prose-p:text-gray-700 prose-a:text-blue-600"
                dangerouslySetInnerHTML={{ __html: mockPost.content }}
              />
            </div>
          </article>

          {/* Navigation */}
          <div className="mt-12 flex justify-between">
            <Button variant="outline" className="hover:bg-blue-50">
              上一篇文章
            </Button>
            <Button variant="outline" className="hover:bg-blue-50">
              下一篇文章
            </Button>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default BlogPost;
