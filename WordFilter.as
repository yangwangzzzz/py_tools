package
{
	public class WordFilter
	{
		public function WordFilter()
		{
		}
		
		private var root:TreeNode;
		
		public function registWords(words:Array):void
		{
			root = new TreeNode();
			root.value = "";
			var wordsLen:int = words.length;
			for (var i:int = 0; i < wordsLen; i++)
			{
				var word:String = words[i];
				var len:int = word.length;
				var currentBranch:TreeNode = root;
				for (var j:int = 0; j < len; j++)
				{
					var char:String = word.charAt(j);
					var tmpNode:TreeNode = currentBranch.getChild(char);
					if (tmpNode)
					{
						currentBranch = tmpNode;
					}
					else
					{
						currentBranch = currentBranch.addChild(char);
					}
				}
				currentBranch.isEnd = true;
			}
		}
		
		public function replaceWord(dirtyWords:String):String
		{
			var char:String;
			var curTree:TreeNode = root;
			var childTree:TreeNode;
			var curEndWordTree:TreeNode;
			var dirtyWord:String;
			
			var c:int = 0;//循环索引
			var endIndex:int = 0;//词尾索引
			var headIndex:int = -1;//敏感词词首索引
			while (c < dirtyWords.length)
			{
				char = dirtyWords.charAt(c);
				childTree = curTree.getChild(char);
				if (childTree)//在树中遍历
				{
					if (childTree.isEnd)
					{
						curEndWordTree = childTree;
						endIndex = c;
					}
					if (headIndex == -1)
					{
						headIndex = c;
					}
					curTree = childTree;
					c++;
				}
				else//跳出树的遍历
				{
					if (curEndWordTree)//如果之前有遍历到词尾，则替换该词尾所在的敏感词，然后设置循环索引为该词尾索引
					{
						dirtyWord = curEndWordTree.getFullWord();
						dirtyWords = dirtyWords.replace(dirtyWord, replace(dirtyWord.length));
						c = endIndex;
					}
					else if (curTree != root)//如果之前有遍历到敏感词非词尾，匹配部分未完全匹配，则设置循环索引为敏感词词首索引
					{
						c = headIndex;
						headIndex = -1;
					}
					curTree = root;
					curEndWordTree = null;
					c++;
				}
			}
			
			//循环结束时，如果最后一个字符满足敏感词词尾条件，此时满足条件，但未执行替换，在这里补加
			if (curEndWordTree)
			{
				dirtyWord = curEndWordTree.getFullWord();
				dirtyWords = dirtyWords.replace(dirtyWord, replace(dirtyWord.length));
			}
			
			return dirtyWords;
		}
		
		public function hasDirtyWords(dirtyWords:String):Boolean
		{
			var char:String;
			var curTree:TreeNode = root;
			var childTree:TreeNode;
			var curEndWordTree:TreeNode;
			
			var c:int = 0;//循环索引
			var endIndex:int = 0;//词尾索引
			var headIndex:int = -1;//敏感词词首索引
			while (c < dirtyWords.length)
			{
				char = dirtyWords.charAt(c);
				childTree = curTree.getChild(char);
				if (childTree)//在树中遍历
				{
					if (childTree.isEnd)
					{
						curEndWordTree = childTree;
						endIndex = c;
					}
					if (headIndex == -1)
					{
						headIndex = c;
					}
					curTree = childTree;
					c++;
				}
				else//跳出树的遍历
				{
					if (curEndWordTree)//如果之前有遍历到词尾，则替换该词尾所在的敏感词，然后设置循环索引为该词尾索引
					{
						c = endIndex;
						return true;
					}
					else if (curTree != root)//如果之前有遍历到敏感词非词尾，匹配部分未完全匹配，则设置循环索引为敏感词词首索引
					{
						c = headIndex;
						headIndex = -1;
					}
					curTree = root;
					curEndWordTree = null;
					c++;
				}
			}
			
			//循环结束时，如果最后一个字符满足敏感词词尾条件，此时满足条件，但未执行替换，在这里补加
			if (curEndWordTree)
			{
				return true;
			}
			return false;
		}
		
		private function replace(len:uint):String
		{
			var replaceWord:String = "";
			for (var i:uint = 0; i < len; i++)
			{
				replaceWord += "*";
			}
			return replaceWord;
		}
	}
}
import flash.utils.Dictionary;

class TreeNode
{
	public function TreeNode()
	{
		dict = new Dictionary();
	}
	
	public var isEnd:Boolean = false;
	
	public var parent:TreeNode;
	public var value:String;
	
	private var dict:Dictionary;
	
	private var _isLeaf:Boolean;
	
	/**
	 *是否是叶子节点
	 */
	public function get isLeaf():Boolean
	{
		var index:int = 0;
		for (var key:String in dict)
		{
			index++;
		}
		_isLeaf = index == 0 
		return _isLeaf;
	}
	
	public function getChild(name:String):TreeNode
	{
		return dict[name];
	}
	
	public function addChild(char:String):TreeNode
	{
		var node:TreeNode = new TreeNode();
		dict[char] = node;
		node.value = char;
		node.parent = this;
		return node;
	}
	
	public function getFullWord():String
	{
		var str:String = this.value;
		var node:TreeNode = this.parent;
		while (node)
		{
			str += node.value;
			node = node.parent;
		}
		return str;
	}
}