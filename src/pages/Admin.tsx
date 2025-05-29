
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Plus, Edit, Trash2, LogOut, Eye } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { toast } from "@/hooks/use-toast";
import ArticleEditor from "@/components/ArticleEditor";

const mockArticles = [
  {
    id: 1,
    title: "探索现代前端开发的最新趋势",
    category: "技术",
    status: "已发布",
    publishDate: "2024-05-29",
    views: 156,
  },
  {
    id: 2,
    title: "人工智能时代的思考",
    category: "思考",
    status: "草稿",
    publishDate: "2024-05-28",
    views: 89,
  },
  {
    id: 3,
    title: "代码之美：编程中的艺术哲学",
    category: "编程",
    status: "已发布",
    publishDate: "2024-05-27",
    views: 234,
  },
];

const Admin = () => {
  const navigate = useNavigate();
  const [showEditor, setShowEditor] = useState(false);
  const [editingArticle, setEditingArticle] = useState(null);
  const [articles, setArticles] = useState(mockArticles);

  useEffect(() => {
    const isLoggedIn = localStorage.getItem("isAdminLoggedIn");
    if (!isLoggedIn) {
      navigate("/admin/login");
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("isAdminLoggedIn");
    toast({
      title: "已退出登录",
      description: "感谢您的使用！",
    });
    navigate("/admin/login");
  };

  const handleNewArticle = () => {
    setEditingArticle(null);
    setShowEditor(true);
  };

  const handleEditArticle = (article) => {
    setEditingArticle(article);
    setShowEditor(true);
  };

  const handleDeleteArticle = (id) => {
    setArticles(articles.filter(article => article.id !== id));
    toast({
      title: "文章已删除",
      description: "文章删除成功",
    });
  };

  const handleSaveArticle = (articleData) => {
    if (editingArticle) {
      // 更新文章
      setArticles(articles.map(article => 
        article.id === editingArticle.id 
          ? { ...article, ...articleData }
          : article
      ));
      toast({
        title: "文章已更新",
        description: "文章更新成功",
      });
    } else {
      // 新建文章
      const newArticle = {
        id: Date.now(),
        ...articleData,
        publishDate: new Date().toISOString().split('T')[0],
        views: 0,
      };
      setArticles([newArticle, ...articles]);
      toast({
        title: "文章已创建",
        description: "新文章创建成功",
      });
    }
    setShowEditor(false);
  };

  if (showEditor) {
    return (
      <ArticleEditor
        article={editingArticle}
        onSave={handleSaveArticle}
        onCancel={() => setShowEditor(false)}
      />
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900">后台管理</h1>
            <div className="flex items-center space-x-4">
              <Button onClick={handleNewArticle} className="bg-blue-600 hover:bg-blue-700">
                <Plus className="mr-2 h-4 w-4" />
                新建文章
              </Button>
              <Button variant="outline" onClick={handleLogout}>
                <LogOut className="mr-2 h-4 w-4" />
                退出登录
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Stats Cards */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-lg text-gray-600">总文章数</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-blue-600">{articles.length}</div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-lg text-gray-600">已发布</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-green-600">
                {articles.filter(a => a.status === "已发布").length}
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-lg text-gray-600">草稿</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-orange-600">
                {articles.filter(a => a.status === "草稿").length}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Articles List */}
        <Card>
          <CardHeader>
            <CardTitle>文章管理</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {articles.map(article => (
                <div key={article.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50">
                  <div className="flex-1">
                    <h3 className="font-semibold text-lg">{article.title}</h3>
                    <div className="flex items-center space-x-4 mt-2 text-sm text-gray-600">
                      <Badge variant={article.status === "已发布" ? "default" : "secondary"}>
                        {article.status}
                      </Badge>
                      <span>{article.category}</span>
                      <span>{article.publishDate}</span>
                      <div className="flex items-center space-x-1">
                        <Eye size={14} />
                        <span>{article.views} 浏览</span>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleEditArticle(article)}
                    >
                      <Edit className="h-4 w-4" />
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleDeleteArticle(article.id)}
                      className="text-red-600 hover:bg-red-50"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  );
};

export default Admin;
