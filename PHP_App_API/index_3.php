<?php
/**
  * wechat php test
  */

//define your token
define("TOKEN", "weixin");
$wechatObj = new wechatCallbackapiTest();
$wechatObj->responseMsg();
//$wechatObj->valid();

class wechatCallbackapiTest
{
    /*public function valid()
    {
        $echoStr = $_GET["echostr"];

        //valid signature , option
        if($this->checkSignature()){
            echo $echoStr;
            exit;
        }
    }*/

    public function responseMsg()
    {
        //get post data, May be due to the different environments
        $postStr = $GLOBALS["HTTP_RAW_POST_DATA"];

        //extract post data
        if (!empty($postStr)){
                
                $postObj = simplexml_load_string($postStr, 'SimpleXMLElement', LIBXML_NOCDATA);
                $RX_TYPE = trim($postObj->MsgType);

                switch($RX_TYPE)
                {
                    case "text":
                        $resultStr = $this->handleText($postObj);
                        break;
                    case "event":
                        $resultStr = $this->handleEvent($postObj);
                        break;
                    default:
                        $resultStr = "Unknow msg type: ".$RX_TYPE;
                        break;
                }
           /* $config=array(
'host'=>SAE_MYSQL_HOST_M,
'port'=>SAE_MYSQL_PORT,
'username'=>SAE_MYSQL_PASS,
'dbname'=>SAE_MYSQL_DB,
'charset'=>'utf8'
);

$link=mysql_connect(SAE_MYSQL_HOST_M.':'.SAE_MYSQL_PORT,SAE_MYSQL_USER,SAE_MYSQL_PASS);


if($link)
{
    mysql_select_db(SAE_MYSQL_DB,$link);
    
}
           $sql = "SELECT * FROM `test_database` WHERE `title` LIKE \'���ν��\' LIMIT 0, 30 ";
           $query=mysql_query($sql);
           $rs= mysql_fetch_array($query);
           $contentStr=$rs ['content'];
            
           $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, $contentStr);*/
                echo $resultStr;
        }else {
            echo "";
            exit;
        }
    }

    public function handleText($postObj)
    {
        $fromUsername = $postObj->FromUserName;
        $toUsername = $postObj->ToUserName;
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
			if(!empty( $keyword ))
        {
            $msgType = "text";
            //$contentStr = "Welcome to wechat world!";
			
			switch($keyword){
                        case 13241074: $contentStr="AA"; break;
                        case 13241075: $contentStr="BB"; break;
                        case 13241076: $contentStr="CC"; break;
                        default: $contentStr="��������ȷ��ѧ��"; break;
                    }
            
			$resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, $msgType, $contentStr);
            echo $resultStr;
        }else{
            echo "Input something...";
        }
    }

    public function handleEvent($object)
    {
        $contentStr = "";
        switch ($object->Event)
        {
            case "subscribe":
                $contentStr = "��л����ע��׿�����ݡ�"."\n"."΢�źţ�zhuojinsz"."\n"."׿Խ���壬�������ݣ�����Ϊ���ṩ���ݱ�������ָ�ϣ����������Ϣ��ѯ������õ�����΢��ƽ̨��"."\n"."Ŀǰƽ̨�������£�"."\n"."��1�� �������������룺��������"."\n"."��2�� �鹫���������룺���ݹ���178"."\n"."��3�� ���룬�����룺����I love you"."\n"."��4�� ������Ϣ��ѯ�������룺���ݹ�ǰ��"."\n"."�������ݣ������ڴ�...";
                break;
            default :
                $contentStr = "Unknow Event: ".$object->Event;
                break;
        }
        $resultStr = $this->responseText($object, $contentStr);
        return $resultStr;
    }
    
    public function responseText($object, $content, $flag=0)
    {
        $textTpl = "<xml>
                    <ToUserName><![CDATA[%s]]></ToUserName>
                    <FromUserName><![CDATA[%s]]></FromUserName>
                    <CreateTime>%s</CreateTime>
                    <MsgType><![CDATA[text]]></MsgType>
                    <Content><![CDATA[%s]]></Content>
                    <FuncFlag>%d</FuncFlag>
                    </xml>";
        $resultStr = sprintf($textTpl, $object->FromUserName, $object->ToUserName, time(), $content, $flag);
        return $resultStr;
    }

    private function checkSignature()
    {
        $signature = $_GET["signature"];
        $timestamp = $_GET["timestamp"];
        $nonce = $_GET["nonce"];    
                
        $token = TOKEN;
        $tmpArr = array($token, $timestamp, $nonce);
        sort($tmpArr);
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