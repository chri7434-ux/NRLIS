(function attachSyntheticCareVocabulary(globalObject) {
  "use strict";

  function deepFreeze(value) {
    Object.freeze(value);
    Object.values(value).forEach((child) => {
      if (child && typeof child === "object" && !Object.isFrozen(child)) {
        deepFreeze(child);
      }
    });
    return value;
  }

  const concepts = [
    {
      id: "need-water",
      domain: "basic_need",
      speechAct: "request",
      canonicalText: "我想喝水",
      compactText: "喝水",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "need-food",
      domain: "basic_need",
      speechAct: "request",
      canonicalText: "我想吃东西",
      compactText: "吃东西",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "need-rest",
      domain: "basic_need",
      speechAct: "request",
      canonicalText: "我想休息",
      compactText: "休息",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "need-toilet",
      domain: "basic_need",
      speechAct: "request",
      canonicalText: "我想去卫生间",
      compactText: "去卫生间",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "routine-wash",
      domain: "daily_routine",
      speechAct: "request",
      canonicalText: "我想洗脸",
      compactText: "洗脸",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "routine-mouth-care",
      domain: "daily_routine",
      speechAct: "request",
      canonicalText: "我想清洁口腔",
      compactText: "清洁口腔",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "routine-clothes",
      domain: "daily_routine",
      speechAct: "request",
      canonicalText: "我想换衣服",
      compactText: "换衣服",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "routine-sit-up",
      domain: "daily_routine",
      speechAct: "request",
      canonicalText: "请帮我坐起来",
      compactText: "坐起来",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "comfort-unwell",
      domain: "physical_comfort",
      speechAct: "state",
      canonicalText: "我不舒服",
      compactText: "不舒服",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "comfort-position",
      domain: "physical_comfort",
      speechAct: "request",
      canonicalText: "请帮我调整姿势",
      compactText: "调整姿势",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "comfort-cold",
      domain: "physical_comfort",
      speechAct: "state",
      canonicalText: "我觉得冷",
      compactText: "冷",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "comfort-hot",
      domain: "physical_comfort",
      speechAct: "state",
      canonicalText: "我觉得热",
      compactText: "热",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "environment-light-on",
      domain: "environment_control",
      speechAct: "request",
      canonicalText: "请把灯打开",
      compactText: "开灯",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "environment-light-off",
      domain: "environment_control",
      speechAct: "request",
      canonicalText: "请把灯关掉",
      compactText: "关灯",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "environment-door-open",
      domain: "environment_control",
      speechAct: "request",
      canonicalText: "请把门打开",
      compactText: "开门",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "environment-door-close",
      domain: "environment_control",
      speechAct: "request",
      canonicalText: "请把门关上",
      compactText: "关门",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "conversation-repeat",
      domain: "conversation_repair",
      speechAct: "repair",
      canonicalText: "请再说一遍",
      compactText: "再说一遍",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "conversation-slower",
      domain: "conversation_repair",
      speechAct: "repair",
      canonicalText: "请说慢一点",
      compactText: "说慢一点",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "conversation-time",
      domain: "conversation_repair",
      speechAct: "repair",
      canonicalText: "请给我一点时间",
      compactText: "给我时间",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "conversation-dont-understand",
      domain: "conversation_repair",
      speechAct: "repair",
      canonicalText: "我没有听懂",
      compactText: "没听懂",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "response-yes",
      domain: "response",
      speechAct: "response",
      canonicalText: "是的",
      compactText: "是",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "response-no",
      domain: "response",
      speechAct: "response",
      canonicalText: "不是",
      compactText: "否",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "response-unsure",
      domain: "response",
      speechAct: "response",
      canonicalText: "我不确定",
      compactText: "不确定",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "response-dont-know",
      domain: "response",
      speechAct: "response",
      canonicalText: "我不知道",
      compactText: "不知道",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "social-stay",
      domain: "social_connection",
      speechAct: "social",
      canonicalText: "请陪我一会儿",
      compactText: "陪我一会儿",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "social-quiet",
      domain: "social_connection",
      speechAct: "social",
      canonicalText: "我想安静一会儿",
      compactText: "安静一会儿",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "social-contact-family",
      domain: "social_connection",
      speechAct: "social",
      canonicalText: "我想联系家人",
      compactText: "联系家人",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "social-thanks",
      domain: "social_connection",
      speechAct: "social",
      canonicalText: "谢谢你",
      compactText: "谢谢",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "leisure-television",
      domain: "leisure",
      speechAct: "request",
      canonicalText: "我想看电视",
      compactText: "看电视",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "leisure-music",
      domain: "leisure",
      speechAct: "request",
      canonicalText: "我想听音乐",
      compactText: "听音乐",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "leisure-photos",
      domain: "leisure",
      speechAct: "request",
      canonicalText: "我想看照片",
      compactText: "看照片",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "leisure-window",
      domain: "leisure",
      speechAct: "request",
      canonicalText: "我想看看窗外",
      compactText: "看窗外",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "assistance-closer",
      domain: "assistance",
      speechAct: "request",
      canonicalText: "请靠近一点",
      compactText: "靠近一点",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "assistance-move-item",
      domain: "assistance",
      speechAct: "request",
      canonicalText: "请把这个移开",
      compactText: "移开这个",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "assistance-pass-item",
      domain: "assistance",
      speechAct: "request",
      canonicalText: "请把这个递给我",
      compactText: "递给我",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "assistance-phone",
      domain: "assistance",
      speechAct: "request",
      canonicalText: "请帮我拿手机",
      compactText: "拿手机",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "control-stop",
      domain: "interaction_control",
      speechAct: "control",
      canonicalText: "请先停一下",
      compactText: "停一下",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "control-continue",
      domain: "interaction_control",
      speechAct: "control",
      canonicalText: "请继续",
      compactText: "继续",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "control-wait",
      domain: "interaction_control",
      speechAct: "control",
      canonicalText: "请等一下",
      compactText: "等一下",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    },
    {
      id: "control-finished",
      domain: "interaction_control",
      speechAct: "control",
      canonicalText: "我说完了",
      compactText: "说完了",
      riskClass: "ordinary_care_low_risk",
      confirmationPolicy: "always_required",
      outputPolicy: "confirmed_visual_only",
      provenance: "curated_synthetic",
      meaningRevision: 1
    }
  ];

  globalObject.NRLIS_CARE_CONFIG = deepFreeze({
    version: "0.2.0",
    architectureVersion: "1.0.0",
    mode: "care_nonresearch",
    dataClassification: "synthetic_no_participant_data",
    languageTag: "zh-CN",
    recording: false,
    persistence: false,
    logging: false,
    externalNetwork: false,
    modelInference: false,
    personalization: "none",
    dialectClaim: "none",
    outputMode: "confirmed_visual_only",
    defaultSurfaceMode: "canonical",
    surfaceModes: ["canonical", "compact"],
    candidateSetPolicy: {
      panelSize: 4,
      ordering: "fixed_versioned",
      generation: "curated_lookup_only",
      modelReranking: false
    },
    safetyPolicy: {
      confirmationRequired: true,
      autoConfirmation: false,
      freeTextGeneration: false,
      careDataResearchReuse: false,
      prohibitedDomains: [
        "emergency_instruction",
        "diagnosis",
        "medication_or_treatment_decision",
        "legal_decision",
        "financial_decision",
        "consent_or_capacity"
      ]
    },
    globalActions: [
      "action-none",
      "action-repeat",
      "action-cancel",
      "action-fallback",
      "action-previous-panel",
      "action-next-panel"
    ],
    semanticDomains: [
      "basic_need",
      "daily_routine",
      "physical_comfort",
      "environment_control",
      "conversation_repair",
      "response",
      "social_connection",
      "leisure",
      "assistance",
      "interaction_control"
    ],
    contexts: [
      {
        id: "basic-needs",
        label: "基本需要",
        hint: "吃喝、休息和日常安排",
        panels: [
          {
            id: "basic-essential",
            label: "吃喝与休息",
            conceptIds: ["need-water", "need-food", "need-rest", "need-toilet"]
          },
          {
            id: "basic-routine",
            label: "日常安排",
            conceptIds: [
              "routine-wash",
              "routine-mouth-care",
              "routine-clothes",
              "routine-sit-up"
            ]
          }
        ]
      },
      {
        id: "comfort",
        label: "舒适与环境",
        hint: "表达感受或调整周围环境",
        panels: [
          {
            id: "comfort-body",
            label: "身体感受",
            conceptIds: [
              "comfort-unwell",
              "comfort-position",
              "comfort-cold",
              "comfort-hot"
            ]
          },
          {
            id: "comfort-environment",
            label: "灯和门",
            conceptIds: [
              "environment-light-on",
              "environment-light-off",
              "environment-door-open",
              "environment-door-close"
            ]
          }
        ]
      },
      {
        id: "conversation",
        label: "交流与回答",
        hint: "修复交流或作简短回答",
        panels: [
          {
            id: "conversation-repair",
            label: "没听清或需要时间",
            conceptIds: [
              "conversation-repeat",
              "conversation-slower",
              "conversation-time",
              "conversation-dont-understand"
            ]
          },
          {
            id: "conversation-response",
            label: "简短回答",
            conceptIds: [
              "response-yes",
              "response-no",
              "response-unsure",
              "response-dont-know"
            ]
          }
        ]
      },
      {
        id: "social",
        label: "陪伴与活动",
        hint: "陪伴、联系和休闲选择",
        panels: [
          {
            id: "social-connection",
            label: "陪伴与联系",
            conceptIds: [
              "social-stay",
              "social-quiet",
              "social-contact-family",
              "social-thanks"
            ]
          },
          {
            id: "social-leisure",
            label: "休闲活动",
            conceptIds: [
              "leisure-television",
              "leisure-music",
              "leisure-photos",
              "leisure-window"
            ]
          }
        ]
      },
      {
        id: "assistance",
        label: "帮助与控制",
        hint: "请求帮助或控制当前互动",
        panels: [
          {
            id: "assistance-practical",
            label: "日常帮助",
            conceptIds: [
              "assistance-closer",
              "assistance-move-item",
              "assistance-pass-item",
              "assistance-phone"
            ]
          },
          {
            id: "assistance-control",
            label: "控制互动",
            conceptIds: [
              "control-stop",
              "control-continue",
              "control-wait",
              "control-finished"
            ]
          }
        ]
      }
    ],
    concepts
  });
})(window);
