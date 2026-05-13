# /learn 命令

## 语法

```
/learn <topic>    启动新学习任务
/learn            恢复上次未完成的学习
/learn status     查看当前进度
/learn stop       中途退出当前学习
/learn stages <N> 修改剩余阶段数（N 范围 1-7）
```

## 行为

### `/learn <topic>`

1. 从 `<topic>` 生成 `slug`
2. 检查 `learning/<slug>/` 是否已存在
   - 若存在，提示用户该主题已有学习记录，询问是继续还是重新开始
3. 创建目录结构和 `progress.json`
4. 进入阶段 0，生成学习路线图
5. 在路线图确认后，根据主题复杂度推荐阶段数
6. 等待用户选择阶段数（接受建议/自定义/使用完整 7 阶段）

### `/learn`（无参数）

1. 扫描 `learning/*/progress.json`
2. 找到 `current_stage < recommended_stages` 且 `stages[current_stage].completed` 为 `false` 的任务
3. 若找到多个，列出供用户选择，显示各任务的推荐阶段数和当前进度
4. 若找到 1 个，直接恢复，显示进度信息
5. 若找到 0 个，提示用户使用 `/learn <topic>` 开始新任务

### `/learn status`

1. 扫描 `learning/*/progress.json`
2. 显示当前任务的面板（包含推荐阶段数和完成进度）
3. 若无进行中任务，提示用户使用 `/learn <topic>` 开始

### `/learn stop`

1. 读取当前任务的 `progress.json`
2. 显示已完成阶段摘要
3. 更新 `recommended_stages` 为 `current_stage`（表示只学到当前阶段）
4. 提示用户进度已保存，可随时恢复

### `/learn stages <N>`

1. 校验 `<N>` 范围：必须为 1-7 之间的整数
   - 若 `<N> < 1`：提示阶段数最少为 1
   - 若 `<N> > 7`：提示阶段数最多为 7
   - 若 `<N>` 非整数：提示请输入整数
2. 读取当前任务的 `progress.json`
3. 更新 `recommended_stages` 为 `<N>`
4. 若已完成阶段数 >= `<N>`，提示学习已完成，建议使用 `/learn stop` 保存进度
5. 否则，提示剩余阶段数已调整（显示新阶段数及剩余阶段）