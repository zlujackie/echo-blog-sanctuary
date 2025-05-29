
import { Heart } from "lucide-react";

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white py-12 mt-20">
      <div className="container mx-auto px-4">
        <div className="text-center">
          <h3 className="text-2xl font-bold mb-4">感谢您的关注</h3>
          <p className="text-gray-400 mb-6 max-w-2xl mx-auto">
            这里是我的个人博客，分享技术见解和生活感悟。如果您觉得内容对您有帮助，欢迎分享给更多朋友。
          </p>
          <div className="flex items-center justify-center space-x-1 text-gray-400">
            <span>Made with</span>
            <Heart className="h-4 w-4 text-red-500" />
            <span>by 张三</span>
          </div>
          <div className="mt-4 text-sm text-gray-500">
            © 2024 我的博客. All rights reserved.
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
