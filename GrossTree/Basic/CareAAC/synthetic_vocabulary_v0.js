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

  globalObject.NRLIS_CARE_CONFIG = deepFreeze({
    version: "0.1.0",
    mode: "care_nonresearch",
    dataClassification: "synthetic_no_participant_data",
    recording: false,
    persistence: false,
    logging: false,
    externalNetwork: false,
    outputMode: "confirmed_visual_only",
    vocabularyKind: "generic_synthetic_phrases",
    globalActions: [
      "action-none",
      "action-repeat",
      "action-cancel",
      "action-fallback"
    ],
    contexts: [
      {
        id: "basic-needs",
        label: "基本需要",
        hint: "饮水、进食和休息",
        candidates: [
          { id: "need-water", text: "我想喝水" },
          { id: "need-food", text: "我想吃东西" },
          { id: "need-rest", text: "我想休息" },
          { id: "need-stop", text: "请先停一下" }
        ]
      },
      {
        id: "comfort",
        label: "身体舒适",
        hint: "只表达感受，不作医疗判断",
        candidates: [
          { id: "comfort-unwell", text: "我不舒服" },
          { id: "comfort-position", text: "请帮我调整姿势" },
          { id: "comfort-cold", text: "我觉得冷" },
          { id: "comfort-hot", text: "我觉得热" }
        ]
      },
      {
        id: "conversation",
        label: "交流节奏",
        hint: "控制谈话速度和轮次",
        candidates: [
          { id: "talk-repeat", text: "请再说一遍" },
          { id: "talk-slower", text: "请说慢一点" },
          { id: "talk-time", text: "请给我一点时间" },
          { id: "talk-dont-understand", text: "我没有听懂" }
        ]
      },
      {
        id: "social",
        label: "陪伴与社交",
        hint: "通用的陪伴选择",
        candidates: [
          { id: "social-stay", text: "请陪我一会儿" },
          { id: "social-quiet", text: "我想安静一会儿" },
          { id: "social-family", text: "我想联系家人" },
          { id: "social-thanks", text: "谢谢你" }
        ]
      }
    ]
  });
})(window);
