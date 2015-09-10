$(document).ready(function(e) {
    // 第一屏按钮弹出框 开始
    $(".bounceInUp").hDialog({
        width: 480,
        height: 295,
        positions: 'center',
        boxBg: "initial"
    });
    
    // Ajax 请求
    $('.aj_submit').unbind('click').click(function() {
        var data = {};
        data['company'] = $('input[name="company"]').val();
        data['personName'] = $('input[name="personName"]').val();
        data['personCount'] = $('input[name="personCount"]').val();
        data['telephone'] = $('input[name="telephone"]').val();
        data['email'] = $('input[name="email"]').val();
        // data['img'] = $('input[name="img"]').val();
        data['captcha'] = $('input[name="captcha"]').val();
        var url = '/user/post';
        var callback = function(){
            alert('提交成功！');
        }
        $.post(url, data, callback);
    });
});
