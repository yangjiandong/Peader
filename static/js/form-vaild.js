// 表格数据检查类
	
var FormValider = {
	
	//获取表格项的的值
	
	initailize : function(form_id, submit_id){
		this.form_id = form_id;
		this.submit = submit_id;
	},
	
	_submit_toggle :function(){
		
	},
	
	_filed_value : function (filed_id){
		return $(filed_id).attr('value');
	},
	
	is_nil : function(filed_id){
		try{
			value = this._field_value(filed_id);
			return (value == null || value == '');
		} catch(e){
			return true;
		}
	},
	
	is_email : function(filed_id){
		try {
			value = this._filed_value(filed_id);
			
            return /^(([^<>( )[\]\\.,;:\s@\"]+(\.[^<>( )[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[(2([0-4]\d|5[0-5])|1?\d{1,2})(\.(2([0-4]\d|5[0-5])| 1?\d{1,2})){3} \])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(value);
        } catch (e) {
            return (false);
        }
	},
	
	
	is_password : function(filed_id,  options){
			pw = this._filed_value(filed_id);
			var o = {
					lower:    0,
					upper:    0,
					alpha:    0, /*大小写*/
					numeric:  0,
					special:  0,
					length:   [6, 16],
					custom:   [ /* 自定义处理方法接口*/ ],
					badWords: [],
					badSequenceLength: 0,
					noQwertySequences: false,
					noSequential:      false
			};

			for (var property in options)
				o[property] = options[property];

			var	re = {
					lower:   /[a-z]/g,
					upper:   /[A-Z]/g,
					alpha:   /[A-Z]/gi,
					numeric: /[0-9]/g,
					special: /[\W_]/g
			},
			rule, i;

			// 密码长度检查
			if (pw.length < o.length[0] || pw.length > o.length[1])
				return false;

			//包含字符检查
			for (rule in re) {
				if ((pw.match(re[rule]) || []).length < o[rule])
				return false;
			}

			//坏密码
			for (i = 0; i < o.badWords.length; i++) {
				if (pw.toLowerCase().indexOf(o.badWords[i].toLowerCase()) > -1)
					return false;
			}
			
			if (o.noSequential && /([\S\s])\1/.test(pw))
				return false;

			//序列重复，坏密码
			if (o.badSequenceLength) {
				var	lower   = "abcdefghijklmnopqrstuvwxyz",
				upper   = lower.toUpperCase(),
				numbers = "0123456789",
				qwerty  = "qwertyuiopasdfghjklzxcvbnm",
				start   = o.badSequenceLength - 1,
				seq     = "_" + pw.slice(0, start);
				for (i = start; i < pw.length; i++) {
					seq = seq.slice(1) + pw.charAt(i);
					if (lower.indexOf(seq)   > -1 ||
						upper.indexOf(seq)   > -1 ||
						numbers.indexOf(seq) > -1 ||
						(o.noQwertySequences && qwerty.indexOf(seq) > -1)) {
							return false;
					}
				}
			}

			// 自定义处理
			for (i = 0; i < o.custom.length; i++) {
				rule = o.custom[i];
				if (rule instanceof RegExp) {
					if (!rule.test(pw))
						return false;
				} else if (rule instanceof Function) {
					if (!rule(pw))
						return false;
				}
			}
			return true;
	},
	
	check_filed : function  (filed_id, type) {
		
		var valided = false;
	  	if(type == "password")
	  		valided = this.is_password(filed_id);
	  	if(type == "email")
	  		valided = this.is_email(filed_id);
	  		
	  	if(valided == false) {
	  		 // $(this.submit).attr('disabled','disabled');
	  		this.report_error(filed_id, type);
	  	} else {
	  		
			this.report_success(filed_id);
		}
		
		return valided;
	},
	
	report_error : function(filed_id, type) {
		
		var error_msg = '';
	  	if(type == "password" )
	  		error_msg = "*密码格式错误，不少于6位，不大于16位";
	  	if(type == "email")
	  		error_msg = "*邮箱格式错误，请正确填写邮箱";
	  		
		var parent = $(filed_id).parent();
		var error_div = document.createElement("div");
		error_div.className = "valid-error";
		var span = document.createElement("span");
		var text = document.createTextNode(error_msg);
		span.appendChild(text);
		error_div.appendChild(span);
		parent.append(error_div);
	},
	
	report_success : function(filed_id) {
		var error_div = $(filed_id).next();
		console.log(error_div);
		if(error_div)
			error_div.remove();
	}
};

