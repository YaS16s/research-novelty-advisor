# Toolkit by domain (Box 4 starting points)

These are starting points, not a finished answer. Confirm that each dataset, library and pretrained model still exists and is maintained (search if unsure), keep only what fits the user's task, hardware and deadline, and add domain items found in the papers you collected. Never list a dataset or tool you cannot name precisely.

## Universal items (every domain)

**Skills, in priority order**
1. Reproducing the baseline exactly (same data split, same metric code). If you cannot reproduce it, nothing else is comparable.
2. Experiment tracking and reproducibility (fixed seeds, config files, logging, Git).
3. Ablation design and fair comparison.
4. Reading and writing papers: related-work mapping, results tables, honest limitations.
5. Statistical validation: multiple seeds, mean and standard deviation, significance tests where differences are small.

**Experiment checklist**
- Reproduce the baseline and report your reproduced number next to the paper's number.
- Compare against the baseline plus 2-4 recent strong methods found in Box 1.
- Ablation: add or remove each new component separately, then in combination.
- Run at least 3 seeds when differences are small; report mean and spread.
- Report cost: parameters, FLOPs or latency, memory, training time.
- Check generalisation on a second dataset or condition.
- Error analysis: show failure cases and say why they fail.
- Release code and configs; state exact versions.

**Writing tips for publication**
- Lead with the contribution that survived the novelty check, not with the architecture diagram.
- State the delta against the closest paper explicitly in the introduction or related work.
- Match the target venue's page limit and style early; check venue deadlines and policies directly.

## Computer vision and deep learning (detection, segmentation, aerial and UAV, multimodal)

- Skills: PyTorch, data pipelines and augmentation, transfer learning and fine-tuning, loss design, multimodal and cross-modal fusion, small-object detection, model efficiency (pruning, quantisation, distillation), deployment on edge hardware.
- Frameworks: PyTorch, torchvision, Ultralytics, MMDetection or Detectron2, Albumentations, ONNX and TensorRT for deployment, Weights & Biases or TensorBoard for tracking.
- Metrics: mAP@0.5, mAP@0.5:0.95, precision, recall, F1, per-class AP, small/medium/large AP, FPS and latency on the target device, parameters, FLOPs.
- Datasets: choose from the datasets used by the papers in Box 1 for the same task, so results are comparable. Search for the benchmark the closest baseline papers report on. Check each dataset's license and download access before planning around it.
- Compute: free tiers (Kaggle, Google Colab) for small runs; a university or cloud GPU for longer runs; mixed precision and smaller image sizes when memory is tight.

## NLP and LLMs

- Skills: Transformers, fine-tuning (full, LoRA and other parameter-efficient methods), prompt and evaluation design, retrieval-augmented generation, dataset curation and annotation quality.
- Frameworks: PyTorch, Hugging Face Transformers, Datasets and PEFT, vLLM for inference, an evaluation harness for standard benchmarks.
- Metrics: task-specific (accuracy, F1, exact match, BLEU, ROUGE, BERTScore), human evaluation or LLM-as-judge with a validation step, robustness and contamination checks.
- Compute: parameter-efficient fine-tuning on a single GPU for small and medium models; budget for evaluation runs, which are often the bottleneck.

## Time series, signals and tabular data

- Skills: feature engineering, leakage-free splits (time-based), classical baselines, sequence models, calibration and uncertainty.
- Frameworks: scikit-learn, XGBoost or LightGBM, PyTorch, statsmodels, Optuna for tuning.
- Metrics: RMSE, MAE, MAPE, AUC, F1, calibration error, plus backtesting across multiple windows.
- Always include strong simple baselines (naive, linear, gradient boosting); beating a weak baseline proves little.

## Other domains

Use the universal items, then derive domain datasets, metrics and tools from the papers collected in Box 1 (look at what they report on and what code they release).
