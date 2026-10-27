---
title: 物品属性上限
description: 对装备应用物品附魔时你会遇到的各项属性上限一览
published: true
date: 2026-10-26T00:00:00.000Z
tags: upgrades, stat limits, bit limits, enchantments
editor: markdown
dateCreated: 2025-11-22T13:14:58.384Z
---

本页用于说明信息，而非模组制作指南或教程。相关教程请查阅 YouTube、d2mods.info、d2rmodding.com 上的正规资料，或到我们的 Discord modding-help 频道提问。

**图例：**

-   Property \= 属性的内部名称
-   Stat \= 物品属性或属性说明（描述文本）
-   Range \= 属性的大致最小 - 最大值
-   Par Rng \= 副参数可取的范围，通常用于选择技能，也能用于其它用途
-   Fraction \= 每级成长类型。若为 8ths，则每级增长量为 min-max/分母

| Property | Stat | Range | Par Rng | Fraction |
| :--- | :--- | ---: | ---: | ---: |
| strength | %+d 点力量 | \-32 \- 223 |  |  |
| energy | %+d 点能量 | \-32 \- 95 |  |  |
| dexterity | %+d 点敏捷 | \-32 \- 95 |  |  |
| vitality | %+d 点体力 | \-32 \- 95 |  |  |
| maxhp | %+d 点生命 | \-32 \- 479 |  |  |
| maxmana | %+d 点法力 | \-32 \- 223 |  |  |
| item_armor_percent | %+d%% 增强防御 | 0 \- 511 |  |  |
| item_maxdamage_percent | %+d%% 增强武器最大伤害 | 0 \- 511 |  |  |
| item_mindamage_percent | %+d%% 增强武器最小伤害 | 0 \- 511 |  |  |
| tohit | %+d 点攻击评级 | 0 \- 1023 |  |  |
| toblock | %d%% 格挡几率提高 | 0 \- 127 |  |  |
| mindamage | %+d 点武器最小伤害 | 0 \- 255 |  |  |
| maxdamage | %+d 点武器最大伤害 | 0 \- 511 |  |  |
| secondary_mindamage | %+d 点武器最小伤害 | 0 \- 255 |  |  |
| secondary_maxdamage | %+d 点武器最大伤害 | 0 \- 511 |  |  |
| damagepercent | %+d%% 增强武器伤害 | 0 \- 255 |  |  |
| manarecoverybonus | %+d%% 法力恢复 | 0 \- 255 |  |  |
| armorclass | %+d 防御 | \-10 \- 2037 |  |  |
| armorclass_vs_missile | %+d 防御（对远程攻击） | 0 \- 511 |  |  |
| armorclass_vs_hth | %+d 防御（对近战） | 0 \- 255 |  |  |
| normal_damage_reduction | 物理伤害降低 %d | 0 \- 63 |  |  |
| magic_damage_reduction | 魔法伤害降低 %d | 0 \- 63 |  |  |
| damageresist | %+d%% 物理伤害减免 | \-200 \- 311 |  |  |
| magicresist | %+d%% 魔法抗性 | \-200 \- 311 |  |  |
| maxmagicresist | %+d%% 魔法抗性上限 | 0 \- 31 |  |  |
| fireresist | %+d%% 火焰抗性 | \-200 \- 311 |  |  |
| maxfireresist | %+d%% 火焰抗性上限 | 0 \- 31 |  |  |
| lightresist | %+d%% 闪电抗性 | \-200 \- 311 |  |  |
| maxlightresist | %+d%% 闪电抗性上限 | 0 \- 31 |  |  |
| coldresist | %+d%% 冰冷抗性 | \-200 \- 311 |  |  |
| maxcoldresist | %+d%% 冰冷抗性上限 | 0 \- 31 |  |  |
| poisonresist | %+d%% 毒素抗性 | \-200 \- 311 |  |  |
| maxpoisonresist | %+d%% 毒素抗性上限 | 0 \- 31 |  |  |
| firemindam | %+d 点武器最小火焰伤害 | 0 \- 255 |  |  |
| firemaxdam | %+d 点武器最大火焰伤害 | 0 \- 511 |  |  |
| lightmindam | %+d 点武器最小闪电伤害 | 0 \- 63 |  |  |
| lightmaxdam | %+d 点武器最大闪电伤害 | 0 \- 1023 |  |  |
| magicmindam | %+d 点武器魔法伤害 | 0 \- 255 |  |  |
| magicmaxdam | %+d 点武器魔法伤害 | 0 \- 511 |  |  |
| coldmindam | %+d 点武器最小冰冷伤害 | 0 \- 255 |  |  |
| coldmaxdam | %+d 点武器最大冰冷伤害 | 0 \- 511 |  |  |
| poisonmindam | %+d 点武器最小毒素伤害 | 0 \- 1023 |  |  |
| poisonmaxdam | %+d 点武器最大毒素伤害 | 0 \- 1023 |  |  |
| lifedrainmindam | %+d%% 每次命中偷取生命 | 0 \- 127 |  |  |
| manadrainmindam | %+d%% 每次命中偷取法力 | 0 \- 127 |  |  |
| hpregen | 生命补给 %+d | \-30 \- 33 |  |  |
| item_maxdurability_percent | %+d%% 提高最大耐久 | \-20 \- 107 |  |  |
| item_maxhp_percent | %+d%% 提高最大生命 | \-10 \- 53 |  |  |
| item_maxmana_percent | %+d%% 提高最大法力 | \-10 \- 53 |  |  |
| item_attackertakesdamage | 攻击者受到 %d 点伤害 | 0 \- 127 |  |  |
| item_goldbonus | %+d%% 怪物额外金币 | \-100 \- 411 |  |  |
| item_magicbonus | %+d%% 物品随出魔法或更优品质的几率 | \-100 \- 411 |  |  |
| item_knockback | 击退 | 0 \- 127 |  |  |
| item_addclassskills | %+d 级 %s 技能 | 0 \- 7 | 0-7 |  |
| item_addexperience | %+d%% 获得的经验 | \-50 \- 461 |  |  |
| item_healafterkill | 每次击杀后 %+d 生命 | 0 \- 127 |  |  |
| item_reducedprices | 商店价格降低 %d%% | 0 \- 127 |  |  |
| item_lightradius | %+d 点光照范围 | \-4 \- 11 |  |  |
| item_req_percent | 需求提高 %d%% | \-100 \- 155 |  |  |
| item_levelreq | %+d 点需求等级 | \-6 \- 249 |  |  |
| item_fasterattackrate | %+d%% 攻击速度加快 | \-20 \- 107 |  |  |
| item_fastermovevelocity | %+d%% 跑/走速度加快 | \-20 \- 107 |  |  |
| item_fastergethitrate | %+d%% 打击恢复加快 | \-20 \- 107 |  |  |
| item_fasterblockrate | %+d%% 格挡速度加快 | \-20 \- 107 |  |  |
| item_fastercastrate | %+d%% 施法速度加快 | \-20 \- 107 |  |  |
| item_singleskill | %+d 级 %s %s | 0 \- 7 | 0-511 |  |
| item_restinpeace | 被击杀的怪物安息 | 0 \- 1 |  |  |
| item_poisonlengthresist | 中毒持续时间降低 %d%% | \-20 \- 235 |  |  |
| item_normaldamage | %+d 点伤害 | \-20 \- 491 |  |  |
| item_howl | %+d%% 击中使怪物逃跑 | 1 \- 128 |  |  |
| item_stupidity | 击中使目标失明 | 0 \- 127 |  |  |
| item_damagetomana | %+d%% 所受伤害转为法力 | 0 \- 63 |  |  |
| item_ignoretargetac | 无视目标防御 | 0 \- 1 |  |  |
| item_fractionaltargetac | -%d%% 目标防御 | 0 \- 127 |  |  |
| item_preventheal | 阻止怪物恢复生命 | 0 \- 127 |  |  |
| item_halffreezeduration | 冰冻持续时间减半 | 0 \- 1 |  |  |
| item_tohit_percent | %+d%% 攻击评级加成 | \-20 \- 491 |  |  |
| item_damagetargetac | 每次命中使怪物防御 %d | \-128 \- \-1 |  |  |
| item_demondamage_percent | %+d%% 对恶魔伤害 | \-20 \- 491 |  |  |
| item_undeaddamage_percent | %+d%% 对不死生物伤害 | \-20 \- 491 |  |  |
| item_demon_tohit | %+d 点攻击评级（对恶魔） | \-128 \- 895 |  |  |
| item_undead_tohit | %+d 点攻击评级（对不死生物） | \-128 \- 895 |  |  |
| item_throwable | 可投掷 | 0 \- 1 |  |  |
| item_allskills | %+d 级所有技能 | 0 \- 7 |  |  |
| item_attackertakeslightdamage | 攻击者受到 %d 点闪电伤害 | 0 \- 31 |  |  |
| item_freeze | 冻结目标 | 0 \- 31 |  |  |
| item_openwounds | %+d%% 造成开放性伤口的几率 | 0 \- 127 |  |  |
| item_crushingblow | %+d%% 造成压碎性打击的几率 | 0 \- 127 |  |  |
| item_kickdamage | %+d 点踢击伤害 | 0 \- 127 |  |  |
| item_manaafterkill | 每次击杀后 %+d 法力 | 0 \- 127 |  |  |
| item_healafterdemonkill | 每次击杀恶魔后 %+d 生命 | 0 \- 127 |  |  |
| item_deadlystrike | %+d%% 致命一击 | 0 \- 127 |  |  |
| item_absorbfire_percent | %+d%% 吸收火焰伤害 | 0 \- 127 |  |  |
| item_absorbfire | 吸收 %+d 点火焰伤害 | 0 \- 127 |  |  |
| item_absorblight_percent | %+d%% 吸收闪电伤害 | 0 \- 127 |  |  |
| item_absorblight | 吸收 %+d 点闪电伤害 | 0 \- 127 |  |  |
| item_absorbmagic_percent | %+d%% 吸收魔法伤害 | 0 \- 127 |  |  |
| item_absorbmagic | 吸收 %+d 点魔法伤害 | 0 \- 127 |  |  |
| item_absorbcold_percent | %+d%% 吸收冰冷伤害 | 0 \- 127 |  |  |
| item_absorbcold | 吸收 %+d 点冰冷伤害 | 0 \- 127 |  |  |
| item_slow | 使目标减速 %d%% | 0 \- 127 |  |  |
| item_aura | 装备时获得 %d 级 %s 光环 | 0 \- 31 | 0-511 |  |
| item_indesctructible | 不可破坏 | 0 \- 1 |  |  |
| item_cannotbefrozen | 无法冰冻 | 0 \- 1 |  |  |
| item_reanimate | %0%% 几率复活为：%1 | 0 \- 127 | 0-1023 |  |
| item_pierce | %+d%% 穿透攻击 | 0 \- 127 |  |  |
| item_magicarrow | 发射魔法箭 | 0 \- 127 |  |  |
| item_explosivearrow | 发射爆炸箭或弩矢 | 0 \- 127 |  |  |
| item_addskill_tab | %+d 级标枪与长矛技能 | 0 \- 7 | 0-65535 |  |
| item_skillonattack | 攻击时有 %d%% 几率施放 %d 级 %s | 0 \- 127 | 0-65535 |  |
| item_skillonkill | 击杀敌人时有 %d%% 几率施放 %d 级 %s | 0 \- 127 | 0-65535 |  |
| item_skillondeath | 死亡时有 %d%% 几率施放 %d 级 %s | 0 \- 127 | 0-65535 |  |
| item_skillonhit | 击中时有 %d%% 几率施放 %d 级 %s | 0 \- 127 | 0-65535 |  |
| item_skillonlevelup | 升级时有 %d%% 几率施放 %d 级 %s | 0 \- 127 | 0-65535 |  |
| item_charge_noconsume | 终结技有 %+d%% 几率不消耗充能 | 0 \- 127 |  |  |
| item_skillongethit | 受击时有 %d%% 几率施放 %d 级 %s | 0 \- 127 | 0-65535 |  |
| item_charged_skill | %d 级 %s（%d/%d 次充能） | 0 \- 65535 | 0-65535 |  |
| item_noconsume | %+d%% 几率不消耗数量 | 0 \- 127 |  |  |
| item_armor_perlevel | %+d 防御 | 0 \- 63 |  | 8ths |
| item_armorpercent_perlevel | %+d%% 增强防御 | 0 \- 63 |  | 8ths |
| item_hp_perlevel | %+d 点生命 | 0 \- 63 |  | 8ths |
| item_mana_perlevel | %+d 点法力 | 0 \- 63 |  | 8ths |
| item_maxdamage_perlevel | %+d 点武器最大伤害 | 0 \- 63 |  | 8ths |
| item_maxdamage_percent_perlevel | %+d%% 增强武器最大伤害 | 0 \- 63 |  | 8ths |
| item_strength_perlevel | %+d 点力量 | 0 \- 63 |  | 8ths |
| item_dexterity_perlevel | %+d 点敏捷 | 0 \- 63 |  | 8ths |
| item_energy_perlevel | %+d 点能量 | 0 \- 63 |  | 8ths |
| item_vitality_perlevel | %+d 点体力 | 0 \- 63 |  | 8ths |
| item_tohit_perlevel | %+d 点攻击评级 | 0 \- 63 |  | 2ths |
| item_tohitpercent_perlevel | %+d%% 攻击评级加成 | 0 \- 63 |  | 2ths |
| item_cold_damagemax_perlevel | %+d 点武器最大冰冷伤害 | 0 \- 63 |  | 8ths |
| item_fire_damagemax_perlevel | %+d 点武器最大火焰伤害 | 0 \- 63 |  | 8ths |
| item_ltng_damagemax_perlevel | %+d 点武器最大闪电伤害 | 0 \- 63 |  | 8ths |
| item_pois_damagemax_perlevel | %+d 点武器最大毒素伤害 | 0 \- 63 |  | 8ths |
| item_resist_cold_perlevel | %+d%% 冰冷抗性 | 0 \- 63 |  | 8ths |
| item_resist_fire_perlevel | %+d%% 火焰抗性 | 0 \- 63 |  | 8ths |
| item_resist_ltng_perlevel | %+d%% 闪电抗性 | 0 \- 63 |  | 8ths |
| item_resist_pois_perlevel | %+d%% 毒素抗性 | 0 \- 63 |  | 8ths |
| item_absorb_cold_perlevel | 吸收 %d 点冰冷伤害 | 0 \- 63 |  | 8ths |
| item_absorb_fire_perlevel | 吸收 %d 点火焰伤害 | 0 \- 63 |  | 8ths |
| item_absorb_ltng_perlevel | 吸收 %d 点闪电伤害 | 0 \- 63 |  | 8ths |
| item_thorns_perlevel | 攻击者受到 %d 点伤害 | 0 \- 31 |  | 8ths |
| item_find_gold_perlevel | %+d%% 怪物额外金币 | 0 \- 63 |  | 8ths |
| item_find_magic_perlevel | %+d%% 物品随出魔法或更优品质的几率 | 0 \- 63 |  | 8ths |
| item_damage_demon_perlevel | %+d%% 对恶魔伤害 | 0 \- 63 |  | 8ths |
| item_damage_undead_perlevel | %+d%% 对不死生物伤害 | 0 \- 63 |  | 8ths |
| item_tohit_demon_perlevel | %+d 点攻击评级（对恶魔） | 0 \- 63 |  | 2ths |
| item_tohit_undead_perlevel | %+d 点攻击评级（对不死生物） | 0 \- 63 |  | 2ths |
| item_crushingblow_perlevel | %+d%% 造成压碎性打击的几率 | 0 \- 63 |  | 8ths |
| item_openwounds_perlevel | %+d%% 造成开放性伤口的几率 | 0 \- 63 |  | 8ths |
| item_kick_damage_perlevel | %+d 点踢击伤害 | 0 \- 63 |  | 8ths |
| item_deadlystrike_perlevel | %+d%% 致命一击 | 0 \- 63 |  | 8ths |
| item_replenish_durability | 每秒修复 %d 点耐久 | 0 \- 63 |  |  |
| item_replenish_quantity | 补充数量 | 0 \- 63 |  |  |
| item_pierce_cold | -%d%% 敌方冰冷抗性 | \-50 \- 205 |  |  |
| item_pierce_fire | -%d%% 敌方火焰抗性 | \-50 \- 205 |  |  |
| item_pierce_ltng | -%d%% 敌方闪电抗性 | \-50 \- 205 |  |  |
| item_pierce_pois | -%d%% 敌方毒素抗性 | \-50 \- 205 |  |  |
| passive_fire_mastery | %+d%% 火焰技能伤害 | \-50 \- 461 |  |  |
| passive_ltng_mastery | %+d%% 闪电技能伤害 | \-50 \- 461 |  |  |
| passive_cold_mastery | %+d%% 冰冷技能伤害 | \-50 \- 461 |  |  |
| passive_pois_mastery | %+d%% 毒素技能伤害 | \-50 \- 461 |  |  |
| passive_fire_pierce | -%d%% 敌方火焰抗性 | 0 \- 255 |  |  |
| passive_ltng_pierce | -%d%% 敌方闪电抗性 | 0 \- 255 |  |  |
| passive_cold_pierce | -%d%% 敌方冰冷抗性 | 0 \- 255 |  |  |
| passive_pois_pierce | -%d%% 敌方毒素抗性 | 0 \- 255 |  |  |
| passive_mag_mastery | %+d%% 魔法技能伤害 | \-50 \- 461 |  |  |
| passive_mag_pierce | -%d%% 敌方魔法抗性 | 0 \- 255 |  |  |
| pl_maxdamage_percent | %+d%% 额外武器最大伤害 | \-100 \- 411 |  |  |
| pl_mindamage_percent | %+d%% 额外武器最小伤害 | \-100 \- 411 |  |  |
| hpregen_perlevel | 生命补给 %+d | \-30 \- 33 |  | 4ths |
| heal_afterhit | 每次命中获得生命 | 0 \- 127 |  |  |
| item_nonclassskill_display | %+d 级 %s（专属技能） | 0 \- 63 | 0-511 |  |
| item_mindamage_perlvl | %+d 点武器最小伤害 | 0 \- 63 |  |  |
| upgrade_minor | 附魔次数：%d / 2 | 0 \- 255 |  |  |
| upgrade_medium | 附魔次数：%d / 3 | 0 \- 255 |  |  |
| upgrade_major | 附魔次数：%d / 5 | 0 \- 255 |  |  |
| upgrade_uber | 附魔次数：%d / 10 | 0 \- 255 |  |  |
| item_elemskillfire | %+d 级火焰技能 | 0 \- 7 | 0-7 |  |
| item_elemskillcold | %+d 级冰冷技能 | 0 \- 7 | 0-7 |  |
| item_elemskilllight | %+d 级闪电技能 | 0 \- 7 | 0-7 |  |
| item_elemskillpoison | %+d 级毒素技能 | 0 \- 7 | 0-7 |  |
| item_elemskillmagic | %+d 级魔法技能 | 0 \- 7 | 0-7 |  |
| item_strength_percent | %+d%% 力量 | \-63 \- 64 |  |  |
| item_dexterity_percent | %+d%% 敏捷 | \-63 \- 64 |  |  |
| item_vitality_percent | %+d%% 体力 | \-63 \- 64 |  |  |
| item_energy_percent | %+d%% 能量 | \-63 \- 64 |  |  |
| pl_maxthrowdmg_percent | %+d%% 额外投掷武器最小伤害 | \-100 \- 411 |  |  |
| pl_minthrowdmg_percent | %+d%% 额外投掷武器最大伤害 | \-100 \- 411 |  |  |
| upgrade_uber_charm_small | 升级次数：%d / 6 | 0 \- 255 |  |  |
| upgrade_uber_charm_large | 升级次数：%d / 10 | 0 \- 255 |  |  |
| item_magic_damagemax_perlevel | %+d 点最大魔法伤害 | 0 \- 63 |  | 8ths |
| passive_dmg_pierce | -%d%% 敌方物理伤害抗性 | 0 \- 255 |  |  |
