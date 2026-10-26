---
title: D2R Reimagined 常见问题
description: 常见问题与解答
published: true
date: 2026-10-26T00:00:00.000Z
tags: faq, 常见问题, 问答, 疑难解答
editor: markdown
dateCreated: 2026-05-13T11:21:23.617Z
---

**问：模组支持 D2R 3.0 的术士（Warlock）和仓库 DLC 吗？**
答：完全支持。我们会紧跟 SnowCo 的最新版本更新，好坏都跟。

**问：没有 DLC 能玩这个模组吗？**
答：可以，模组在没有 DLC 的情况下 100% 兼容。先驱（Heralds）会刷出，世界之石碎片和雕像会掉落，超级远古者也进得去。

**问：DLC 页签里的堆叠上限能提高到 99 以上吗？**
答：可以用 D2RLoader 把仓库堆叠上限提到 255。除此之外不行，这是引擎限制。

**问：下一个天梯什么时候开？**
答：很快™，预告直播的链接会发在 Discord 里。

**问：能不能让编年史（Chronicle）支持模组新增的暗金和套装物品？**
答：不行。SnowCo 把原版之外的条目限制在超出 200-300 条左右，再多就会持续崩溃，而我们加了接近 1000 条。有脚本可以[直接 100% 点亮](https://discord.com/channels/898562996715012096/910921404571070515/1502460774860197940)，但请先看清楚说明。

答 2：你可以用 D2RLoader，它修复了暴雪编年史的问题，不过你需要重新给物品打上「可编年史」标记。

**问：模组兼容 Steam 吗？**
答：兼容。用桌面启动器或手动安装，[操作步骤见这里](https://wiki.d2r-reimagined.com/en/Installs)。

**问：为什么我没有「Play」按钮？**
答：看你角色列表的右上角，如果那里的文字是「红色」，点一下它会变成金色，然后 Play 按钮就会出现。

**问：有终局玩法吗？**
答：目前没有，但正在开发中，会在十月中旬的公布直播里揭晓。在那之前，我们提供的是[强化过的噩梦、地狱和恐惧地带](https://wiki.d2r-reimagined.com/en/new_player_guide#gameplay-changes)。

**问：能不能让旋风斩（WW）在攻击/命中时的 CTC 生效、每帧判定、加上飞弹或法术，或者让它附带别的效果？**
答：不行。这个技能是深度硬编码的。不过你可以用 D2RLoader 的扩展来调整它。

**问：为什么我的法力是 0、药水没用、找阿卡拉或其他治疗商人也没用？**
答：[护身符重量系统](https://wiki.d2r-reimagined.com/en/Items/Charms#charm-weight-system)允许你放半个背包的护身符，超过之后法力就会被归零。

**问：为什么我捡不起这枚暗金护身符？**
答：你的人物仓库、赫拉迪克方块或背包里已经有一枚掉落过的同款护身符了。把同尺寸的暗金护身符放进共享仓库页签或者丢到地上，就能捡起并鉴定新的那枚。

**问：海法斯特会带光环刷出吗？**
答：不会，这个一年多前在模组 2.0 就去掉了。他不会再以「光环强化」形式刷出，因为那让他和他的小怪太恶心了。

**问：能多加几页共享仓库/页签吗？**
答：可以用 D2RLoader 增加额外的共享仓库页。除此之外不行，这是账号绑定功能，已经无法通过软改模组实现了。

**问：能让光环在左键使用吗？**
答：用 D2RLoader 的扩展可以。除此之外不行，它们不会激活，这是引擎限制。

**问：模组新增的恶魔能被术士奴役（Bound）吗？**
答：不能，它们本来就不打算被奴役。

**问：模组支持多人联机吗？**
答：现在可以通过 D2RLoader 支持多人。用我们的 Reimagined 启动器可以很轻松地下载并使用 D2RLoader。

**问：天梯活动结束后我的角色会怎样？**
答：你可以手动把存档从天梯搬到非天梯：把角色 **.d2s** 文件从天梯目录复制到非天梯存档目录。共享仓库是 **.d2i** 文件，但它会覆盖你现有的非天梯共享仓库。

```
角色存档位置：
天梯：
C:\Users\<你的用户名>\Saved Games\Diablo II Resurrected\mods\ReimaginedThree-Ladder-Slam-<hash-value-here>

非天梯：
C:\Users\<你的用户名>\Saved Games\Diablo II Resurrected\mods\ReimaginedThree
```

**问：怎么在非天梯的 D2RLoader 选项里用上天梯的扩展？**
答：扩展位于你的 D2R 安装目录下的 ```"Diablo II Resurrected/mods/ReimaginedLadder/d2rloader/plugins``` 和 /patches 里。有些扩展还需要 /config 里的文件。

最稳妥的做法是把天梯目录里的 d2rloader 文件夹整个复制到 mods/Reimagined 下，或者挑着复制 plugins/patches，也可以从 d2rloader.net/hub 再拿一些。

**问：D2RLoader 的扩展/插件/补丁去哪里下？**
答：https://d2rloader.net/hub，或者 d2rloader 的 Discord 里会有扩展链接，如果作者还没上架 hub，那里也会有他们的 GitHub。

**问：游戏启动后 Play 按钮下面没有红色齿轮，是坏了吗？**
答：因为 SnowCo 又 SnowCo 了。在命令行加上 `-forcedesktop` 试试，看看能不能神奇地恢复正常。
