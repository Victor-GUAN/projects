<?php
/**
  * wechat php test
  */

//define your token
define("TOKEN", "weixin");
$wechatObj = new wechatCallbackapiTest();
//$wechatObj->valid();
$wechatObj->responseMsg();
class wechatCallbackapiTest
{
	public function valid()
    {
        $echoStr = $_GET["echostr"];

        //valid signature , option
        if($this->checkSignature()){
        	echo $echoStr;
        	exit;
        }
    }

    public function responseMsg()
    {
		//get post data, May be due to the different environments
		$postStr = $GLOBALS["HTTP_RAW_POST_DATA"];

      	//extract post data
		if (!empty($postStr)){
                /* libxml_disable_entity_loader is to prevent XML eXternal Entity Injection,
                   the best way is to check the validity of xml by yourself */
                //libxml_disable_entity_loader(true);
              	$postObj = simplexml_load_string($postStr, 'SimpleXMLElement', LIBXML_NOCDATA);
                $fromUsername = $postObj->FromUserName;
                $toUsername = $postObj->ToUserName;
				$type = $postObj->MsgType;
				$customevent = $postObj->Event;
				$latitude = $postObj->Location_X;
				$longtitude = $postObj->Location_Y;				
                $keyword = trim($postObj->Content);
                $time = time();
                $textTpl = "<xml>
							<ToUserName><![CDATA[%s]]></ToUserName>
							<FromUserName><![CDATA[%s]]></FromUserName>
							<CreateTime>%s</CreateTime>
							<MsgType><![CDATA[%s]]></MsgType>
							<Content><![CDATA[%s]]></Content>
							<FuncFlag>0</FuncFlag>
							</xml>";    
				switch ($type)
				{	case "event";
				if ($customevent=="subscribe")
					{$contentStr = "感谢您的关注";}
				break;
				case "image";
				$contentStr = "暂不支持图片解析功能，请输入正确信息";
				break;
				case "link";
				$contentStr = "暂不支持超链接解析功能，请输入正确信息";
				case "text";
					switch($keyword)
					{
						case "1";
						$contentStr = "现在可以查询成绩，请输入学号";
						break;
						default;
						include("conn.php");
						$sql = "SELECT * FROM `weixin` WHERE `title` LIKE '%{$keyword}%' LIMIT 0 , 30";
						$query=mysql_query($sql);
						$rs=mysql_fetch_array($query);
						$contentStr=$rs['content'];
						
						mysql_close($conn);
					}
					break;
					default;
					$contentStr ="请输入正确信息";
					}
					$resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, $contentStr);						
					echo $resultStr;
					
					
        }else {
        	echo "";
        	exit;
        }
    }
		
	private function checkSignature()
	{
        // you must define TOKEN by yourself
        if (!defined("TOKEN")) {
            throw new Exception('TOKEN is not defined!');
        }
        
        $signature = $_GET["signature"];
        $timestamp = $_GET["timestamp"];
        $nonce = $_GET["nonce"];
        		
		$token = TOKEN;
		$tmpArr = array($token, $timestamp, $nonce);
        // use SORT_STRING rule
		sort($tmpArr, SORT_STRING);
		$tmpStr = implode( $tmpArr );
		$tmpStr = sha1( $tmpStr );
		
		if( $tmpStr == $signature ){
			return true;
		}else{
			return false;
		}
	}
}

?>