/**
 * DAT System - i18n Translation Engine
 * Lightweight: no dependencies, single dictionary, localStorage persistence.
 */

(function () {
  "use strict";

  // ---- State ----
  window.__lang = localStorage.getItem("dat_lang") || "zh";

  // ---- Dictionary ----
  const DICT = {
    zh: {},
    en: {},
  };

  // Shorthand
  function Z(k, v) { DICT.zh[k] = v; }
  function E(k, v) { DICT.en[k] = v; }
  function B(k, zh, en) { DICT.zh[k] = zh; DICT.en[k] = en; }

  // ====== COMMON ======
  B("common.loading", "加载中...", "Loading...");
  B("common.save", "保存", "Save");
  B("common.cancel", "取消", "Cancel");
  B("common.confirm", "确认", "Confirm");
  B("common.delete", "删除", "Delete");
  B("common.search", "搜索", "Search");
  B("common.back", "返回", "Back");
  B("common.close", "关闭", "Close");
  B("common.error", "操作失败", "Operation failed");
  B("common.success", "操作成功", "Success");
  B("common.not_found", "未找到", "Not found");
  B("common.no_data", "暂无数据", "No data");

  // ====== NAVBAR ======
  B("nav.brand", "DAT System", "DAT System");
  B("nav.intro", "任务介绍", "Introduction");
  B("nav.test", "开始测试", "Test");
  B("nav.results", "结果查询", "Results");
  B("nav.analysis", "数据分析", "Analysis");
  B("nav.admin", "管理", "Admin");
  B("nav.logout", "退出", "Logout");
  B("nav.switch_lang", "EN", "中文");
  B("nav.user", "用户", "User");

  // ====== LOGIN ======
  B("login.title", "发散性思维测试", "Divergent Thinking Test");
  B("login.subtitle", "Divergent Association Task", "Divergent Association Task");
  B("login.username", "用户名", "Username");
  B("login.password", "密码", "Password");
  B("login.username_placeholder", "请输入用户名", "Enter username");
  B("login.password_placeholder", "请输入密码", "Enter password");
  B("login.submit", "登录", "Login");
  B("login.logging_in", "登录中...", "Logging in...");
  B("login.no_account", "没有账号？", "No account? ");
  B("login.register_link", "注册新账号", "Register");
  B("login.error_empty", "请输入用户名和密码", "Please enter username and password");
  B("login.error_failed", "登录失败，请检查用户名和密码", "Login failed. Check username and password");
  B("login.paper_citation",
    "基于论文：Ding, G., He, Y., Yi, K., & Li, S. (2024).",
    "Based on: Ding, G., He, Y., Yi, K., & Li, S. (2024).");

  // ====== REGISTER ======
  B("register.title", "注册账号", "Register");
  B("register.subtitle", "创建 DAT System 账号", "Create DAT System account");
  B("register.username", "用户名", "Username");
  B("register.password", "密码", "Password");
  B("register.password_placeholder", "至少6位字符", "At least 6 characters");
  B("register.confirm_password", "确认密码", "Confirm Password");
  B("register.confirm_placeholder", "再次输入密码", "Re-enter password");
  B("register.submit", "注册", "Register");
  B("register.has_account", "已有账号？", "Already have an account? ");
  B("register.login_link", "返回登录", "Back to Login");
  B("register.error_mismatch", "两次输入密码不一致", "Passwords do not match");
  B("register.error_failed", "注册失败", "Registration failed");
  B("register.success", "注册成功，请登录", "Registered! Redirecting to login...");

  // ====== INTRODUCTION ======
  B("intro.title", "发散性关联任务（DAT）", "Divergent Association Task (DAT)");
  B("intro.desc", "通过计算词汇之间的语义距离，客观测量发散性思维水平",
    "Measuring divergent thinking objectively through semantic distance between words.");
  B("intro.paper",
    "本系统基于论文：",
    "This system is based on the paper:");
  B("intro.what_is.title", "什么是发散性思维", "What is Divergent Thinking");
  B("intro.what_is.body",
    "发散性思维是创造性思维的核心组成部分，指个体在面对开放性问题时，产生多种不同想法和解决方案的能力。与寻找唯一正确答案的聚合性思维不同，发散性思维强调思维的广度与灵活性。",
    "Divergent thinking is a core component of creative thinking — the ability to generate multiple diverse ideas and solutions to open-ended problems. Unlike convergent thinking which seeks a single correct answer, divergent thinking emphasizes breadth and flexibility of thought.");
  B("intro.principle.title", "测量原理", "How It Works");
  B("intro.principle.body",
    "DAT 基于联想创造性理论：能够将语义距离较远的概念联系起来的人，往往具有更强的发散性思维能力。系统使用自然语言处理模型（Word2Vec）将词汇转换为向量，计算词汇之间的余弦距离，距离越远说明思维越具发散性。",
    "DAT is based on the Associative Theory of Creativity: people who can connect semantically distant concepts tend to have stronger divergent thinking. The system uses NLP models (Word2Vec) to convert words into vectors and compute cosine distances — greater distance indicates more divergent thinking.");
  B("intro.steps.title", "操作步骤", "Steps");
  B("intro.step1.title", "进入测试", "Start the Test");
  B("intro.step1.desc", "点击「开始测试」，系统开始计时", "Click \"Test\" to begin. The timer starts immediately.");
  B("intro.step2.title", "输入10个名词", "Enter 10 Nouns");
  B("intro.step2.desc", "在规定时间内，输入10个尽可能互不相关的名词", "Enter 10 nouns that are as unrelated to each other as possible.");
  B("intro.step3.title", "查看结果", "View Results");
  B("intro.step3.desc", "提交后查看 DAT 得分和语义距离热力图", "After submission, view your DAT score and semantic distance heatmap.");
  B("intro.tips.title", "小提示", "Tips");
  B("intro.tips.1", "请确保输入的都是名词", "Make sure all entries are nouns");
  B("intro.tips.2", "词汇差异越大越好（如「河流」和「电脑」），避免同类词（如「苹果」和「香蕉」）",
    "Greater difference is better (e.g. \"river\" and \"computer\"), avoid similar words (e.g. \"apple\" and \"banana\")");
  B("intro.tips.3", "不在词库中的词汇会被自动跳过，不影响总分", "Words not in the vocabulary are skipped automatically");
  B("intro.tips.4", "至少需要 5 个有效词汇才能生成热力图", "At least 5 valid words needed for heatmap generation");
  B("intro.start_btn", "开始测试", "Start Test");

  // ====== TEST PAGE ======
  B("test.title", "发散性思维测试", "Divergent Thinking Test");
  B("test.enter_words", "请输入 10 个互不相关的名词", "Enter 10 unrelated nouns");
  B("test.time_remaining", "剩余时间", "Time Remaining");
  B("test.rule_card",
    "词汇差异越大得分越高。必须输入名词，不填动词或形容词。至少 5个有效词 可生成热力图。",
    "Greater difference = higher score. Enter NOUNS only. At least 5 valid words for heatmap.");
  B("test.input_placeholder", "输入名词...", "Enter a noun...");
  B("test.submit_btn", "提交答案", "Submit");
  B("test.retry_btn", "重新测试", "Retry");
  B("test.history_btn", "查看历史记录", "View History");
  B("test.pretest_time_prefix", "请在", "Please enter 10 unrelated nouns within ");
  B("test.pretest_time_suffix", " 内输入 10个互不相关的名词", "");
  B("test.pretest_time_suffix_en", "", " minutes");
  B("test.pretest_tip1", "词汇之间的差异越大越好。例如：「大海」和「数学」的距离很远，「苹果」和「香蕉」的距离很近。",
    "The more different the words, the better. E.g. \"ocean\" and \"math\" are far apart, \"apple\" and \"banana\" are close.");
  B("test.pretest_tip2", "请确保输入的是名词，不是动词或形容词。", "Make sure to enter nouns, not verbs or adjectives.");
  B("test.pretest_tip3", "系统会过滤无效词汇，至少需要 5个有效词 才能生成热力图。",
    "Invalid words are filtered. At least 5 valid words needed for heatmap.");
  B("test.start_btn", "开始作答", "Start");
  B("test.calculating", "正在计算得分...", "Calculating score...");
  B("test.config_failed", "获取配置失败", "Failed to load configuration");
  B("test.time_up", "时间到，自动提交", "Time is up. Auto-submitting...");
  B("test.error_empty", "请至少输入一个词汇", "Please enter at least one word");
  B("test.error_calc_failed", "计算失败：", "Calculation failed: ");
  B("test.score_label", "DAT 得分", "DAT Score");
  B("test.effective_words", "有效词汇", "Valid Words");
  B("test.over_percent", "超越", "Better than ");
  B("test.over_percent_suffix", "% 的用户", "% of users");
  B("test.heatmap_title", "语义距离热力图", "Semantic Distance Heatmap");
  B("test.heatmap_legend", "深红 = 距离近 · 深蓝 = 距离远", "Dark Red = Close · Dark Blue = Far");
  B("test.heatmap_tooltip_dist", "语义距离:", "Distance:");
  B("test.heatmap_far", "远", "Far");
  B("test.heatmap_close", "近", "Close");
  B("test.heatmap_no_data", "有效词汇不足，无法生成热力图", "Not enough valid words for heatmap");
  B("test.model_label", "模型：", "Model: ");
  B("test.minute_unit", "分", " min ");
  B("test.second_unit", "秒", " sec");

  // ====== RESULTS ======
  B("results.title", "作答记录", "Test Records");
  B("results.new_test", "新建测试", "New Test");
  B("results.search_placeholder", "搜索用户名...", "Search username...");
  B("results.search_btn", "搜索", "Search");
  B("results.th_id", "ID", "ID");
  B("results.th_username", "用户名", "Username");
  B("results.th_time", "时间", "Time");
  B("results.th_score", "得分", "Score");
  B("results.th_valid", "有效词", "Valid");
  B("results.view_btn", "查看", "View");
  B("results.empty", "暂无作答记录", "No test records yet");
  B("results.start_first", "开始第一次测试", "Take your first test");
  B("results.load_failed", "加载失败", "Failed to load");

  // ====== RESULT DETAIL ======
  B("detail.title", "结果详情", "Result Detail");
  B("detail.back_list", "返回列表", "Back to List");
  B("detail.score_label", "DAT 得分", "DAT Score");
  B("detail.over_percent", "超越", "Better than ");
  B("detail.over_percent_suffix", "% 的用户", "% of users");
  B("detail.effective_words", "有效词汇", "Valid Words");
  B("detail.words_section", "作答词汇", "Submitted Words");
  B("detail.empty_word", "空", "Empty");
  B("detail.info_section", "测试信息", "Test Info");
  B("detail.info_user", "用户", "User");
  B("detail.info_time", "时间", "Time");
  B("detail.info_spent", "作答耗时", "Time Spent");
  B("detail.info_spent_unit", "秒", " sec");
  B("detail.info_limit", "限制时间", "Time Limit");
  B("detail.info_limit_unit", "秒", " sec");
  B("detail.heatmap_title", "语义距离热力图", "Semantic Distance Heatmap");
  B("detail.heatmap_legend", "深红 = 距离近 · 深蓝 = 距离远", "Dark Red = Close · Dark Blue = Far");
  B("detail.heatmap_tooltip", "语义距离:", "Distance:");
  B("detail.heatmap_far", "远", "Far");
  B("detail.heatmap_close", "近", "Close");
  B("detail.heatmap_no_data", "有效词汇不足，无法生成热力图", "Not enough valid words for heatmap");
  B("detail.load_failed", "加载失败", "Failed to load");
  B("detail.not_found", "缺少记录 ID", "Missing record ID");

  // ====== ANALYSIS ======
  B("analysis.title", "数据分析", "Data Analysis");
  B("analysis.sample_count", "样本数", "Sample Size");
  B("analysis.avg", "平均分", "Average");
  B("analysis.max", "最高分", "Maximum");
  B("analysis.min", "最低分", "Minimum");
  B("analysis.median", "中位数", "Median");
  B("analysis.std", "标准差", "Std Dev");
  B("analysis.load_failed", "加载失败", "Failed to load");

  // ====== ADMIN ======
  B("admin.title", "管理面板", "Admin Panel");
  B("admin.upload_users", "批量上传用户", "Batch Upload Users");
  B("admin.upload_users_desc", "通过 Excel 文件导入用户", "Import users via Excel file");
  B("admin.task_config", "任务时间配置", "Task Time Config");
  B("admin.task_config_desc", "调整测试限制时间", "Adjust test time limit");
  B("admin.data_analysis", "数据分析", "Data Analysis");
  B("admin.data_analysis_desc", "查看统计分析", "View statistics");
  B("admin.model_config", "Embedding 模型", "Embedding Models");
  B("admin.model_config_desc", "配置词向量模型", "Configure embedding models");
  B("admin.export_csv", "导出 CSV", "Export CSV");
  B("admin.export_csv_desc", "下载作答记录为 CSV", "Download records as CSV");
  B("admin.export_xlsx", "导出 Excel", "Export Excel");
  B("admin.export_xlsx_desc", "下载作答记录为 Excel", "Download records as Excel");
  B("admin.change_password", "修改密码", "Change Password");
  B("admin.change_password_desc", "修改当前用户密码", "Change current user password");
  B("admin.old_password", "旧密码", "Old Password");
  B("admin.new_password", "新密码", "New Password");
  B("admin.confirm_password", "确认新密码", "Confirm New Password");
  B("admin.pwd_mismatch", "两次输入不一致", "Passwords do not match");
  B("admin.pwd_changed", "密码已修改", "Password changed");
  B("admin.export_toast", "正在导出...", "Exporting...");

  // ====== UPLOAD USERS ======
  B("upload.title", "批量上传用户", "Batch Upload Users");
  B("upload.back", "返回", "Back");
  B("upload.upload_btn", "上传导入", "Upload & Import");
  B("upload.choose_file", "选择文件", "Choose File");
  B("upload.file_hint", "Excel 文件需包含 username 和 password 列。", "Excel file must contain 'username' and 'password' columns.");
  B("upload.template_title", "模板示例", "Template Example");
  B("upload.error_no_file", "请选择文件", "Please select a file");
  B("upload.error_upload", "上传失败", "Upload failed");

  // ====== TASK CONFIG ======
  B("taskconfig.title", "任务时间配置", "Task Time Config");
  B("taskconfig.back", "返回", "Back");
  B("taskconfig.limited_time", "限制时间（秒）", "Time Limit (seconds)");
  B("taskconfig.hint", "建议 60-600 秒，默认 240 秒（4分钟）", "Recommended 60-600 sec, default 240 sec (4 min)");
  B("taskconfig.error_range", "时间范围 10-3600 秒", "Must be between 10 and 3600 seconds");
  B("taskconfig.saved", "已更新为", "Updated to ");
  B("taskconfig.seconds", "秒", " sec");

  // ====== MODEL CONFIG ======
  B("modelconfig.title", "Embedding 模型配置", "Embedding Model Config");
  B("modelconfig.back", "返回", "Back");
  B("modelconfig.current", "当前模型", "Current Model");
  B("modelconfig.active", "已激活的模型", "Active Models");
  B("modelconfig.active_empty", "暂无已激活的 API 模型（Word2Vec 默认可用）", "No API models activated (Word2Vec is always available)");
  B("modelconfig.current_tag", "当前", "Active");
  B("modelconfig.switch_btn", "切换", "Switch");
  B("modelconfig.templates", "内置模型模板", "Built-in Model Templates");
  B("modelconfig.templates_hint", "选择一个模型并填入 API Key 即可激活使用。", "Select a model and enter an API Key to activate it.");
  B("modelconfig.activated", "已激活", "Activated");
  B("modelconfig.activate_btn", "激活", "Activate");
  B("modelconfig.custom_title", "添加自定义模型", "Add Custom Model");
  B("modelconfig.custom_hint", "支持任何兼容 OpenAI API 格式的 Embedding 服务。", "Supports any OpenAI-compatible embedding API.");
  B("modelconfig.custom_name", "显示名称", "Display Name");
  B("modelconfig.custom_name_ph", "如：我的模型", "e.g. My Model");
  B("modelconfig.custom_dim", "向量维度", "Dimension");
  B("modelconfig.custom_dim_ph", "如：1536", "e.g. 1536");
  B("modelconfig.custom_url", "API 地址", "API Base URL");
  B("modelconfig.custom_url_ph", "https://api.example.com/v1", "https://api.example.com/v1");
  B("modelconfig.custom_model_id", "模型 ID", "Model ID");
  B("modelconfig.custom_model_id_ph", "model-name", "model-name");
  B("modelconfig.custom_key", "API Key", "API Key");
  B("modelconfig.custom_key_ph", "sk-...", "sk-...");
  B("modelconfig.custom_submit", "添加模型", "Add Model");
  B("modelconfig.prompt_title", "输入 API Key 以激活：", "Enter API Key to activate:");
  B("modelconfig.delete_confirm", "确定移除模型", "Confirm remove model ");
  B("modelconfig.delete_confirm_suffix", "？", "?");
  B("modelconfig.cache_title", "向量缓存", "Vector Cache");
  B("modelconfig.cache_empty", "缓存为空", "Cache is empty");
  B("modelconfig.cache_entry", "个词向量", " cached vectors");
  B("modelconfig.load_failed", "加载失败", "Failed to load");
  B("modelconfig.switch_ok", "已切换", "Switched");
  B("modelconfig.activated_ok", "已激活", "Activated");
  B("modelconfig.added_ok", "已添加", "Added");
  B("modelconfig.removed_ok", "已移除", "Removed");

  // ====== API / JS ERRORS ======
  B("api.request_failed", "请求失败", "Request failed");
  B("api.unauthorized", "未授权", "Unauthorized");
  B("api.forbidden", "无权限", "Forbidden");

  // ====== DATE LOCALE ======
  B("date.locale", "zh-CN", "en-US");

  // ---- Public API ----
  window.t = function (key, replacements) {
    let lang = window.__lang;
    let val = (DICT[lang] && DICT[lang][key]) || (DICT.zh && DICT.zh[key]) || key;
    if (replacements) {
      for (const k in replacements) {
        val = val.replace("{" + k + "}", replacements[k]);
      }
    }
    return val;
  };

  window.getLang = function () {
    return window.__lang;
  };

  window.setLang = function (lang) {
    window.__lang = lang;
    localStorage.setItem("dat_lang", lang);
    document.documentElement.lang = lang === "zh" ? "zh-CN" : "en";
  };

  window.toggleLang = function () {
    const next = window.__lang === "zh" ? "en" : "zh";
    setLang(next);
    window.location.reload();
  };

  window.applyI18n = function (root) {
    root = root || document;
    const els = root.querySelectorAll("[data-i18n]");
    els.forEach(function (el) {
      const key = el.getAttribute("data-i18n");
      if (key) el.textContent = window.t(key);
    });
    // Also handle placeholders
    const phEls = root.querySelectorAll("[data-i18n-placeholder]");
    phEls.forEach(function (el) {
      const key = el.getAttribute("data-i18n-placeholder");
      if (key) el.placeholder = window.t(key);
    });
  };

  // Apply lang attribute on load
  document.documentElement.lang = window.__lang === "zh" ? "zh-CN" : "en";
})();
