## 🛠️ Installation and Usage

### Prerequisites

- Python 3.9+
- Gemini API key (for LLM evaluation)
- Jina API key (for web scraping in FACT evaluation)

### Setup

```bash
git clone https://github.com/your-username/deep_research_bench.git
cd deep_research_bench
pip install -r requirements.txt
```

### API Configuration

Set the required API keys as environment variables:

```bash
# Set Gemini API key for LLM evaluation
export GEMINI_API_KEY="your_gemini_api_key_here"

# Set Jina API key for web scraping
export JINA_API_KEY="your_jina_api_key_here"
```


## Project Structure

```
deep_research_bench/
├── data/
│   ├── criteria_data/      # Evaluation criteria data
│   ├── prompt_data/        
│   │   └── query.jsonl     # ← 100 benchmark queries for your agent
│   └── test_data/          
│       ├── cleaned_data/   # Cleaned article data
│       └── raw_data/       # ← Put your model outputs here (model_name.jsonl)
├── prompt/                 # Prompt templates
├── utils/                  # Utility functions
├── deepresearch_bench_race.py  # RACE evaluation script
├── run_benchmark.sh        # ← Add your model names here, then run
└── requirements.txt        # Dependencies
```

**Quick Start Flow:**
1. Use queries from `data/prompt_data/query.jsonl` → Run your Deep Research Agent
2. Save outputs to `data/test_data/raw_data/<model_name>.jsonl`
3. Add model name to `TARGET_MODELS` in `run_benchmark.sh`
4. Run: `bash run_benchmark.sh`

## Quick Start

### 1. Prepare Your Model Data

Run your Deep Research Agent on the benchmark queries and save outputs in the required format:

**Input**: Use queries from `data/prompt_data/query.jsonl` (100 benchmark tasks)

**Output**: Save results to `data/test_data/raw_data/<model_name>.jsonl`

**Required format** (each line should contain):
```json
{
    "id": "task_id", 
    "prompt": "original_query_text", 
    "article": "generated_research_article_with_citations"
}
```

### 2. Configure Models to Evaluate

Edit `run_benchmark.sh` and add your model name:
```bash
TARGET_MODELS=("your-model-name")
```

### 3. Run Evaluation

```bash
bash run_benchmark.sh
```

Results will be saved to:
- RACE evaluation: `results/race/<model_name>/race_result.txt`
- FACT evaluation: `results/fact/<model_name>/fact_result.txt`

### RACE scoring modes: pairwise (default) vs `--no_reference`

- **Default (pairwise) RACE**: compares your model's article against a reference article.
  - Requires `data/test_data/cleaned_data/reference.jsonl`.
  - Score calculation:
    - **Overall**: `target_total / (target_total + reference_total)`.
    - **Per-dimension**: `target_dim / (target_dim + reference_dim)`.
  - Outputs are in the 0–1 range.

- **No-reference mode**: run RACE without any reference article by using `--no_reference`.
  - The script skips loading `reference.jsonl` and uses a single-article scoring prompt.
  - Score normalization keeps outputs in 0–1 by dividing by 10 (max per-dimension score):
    - **Overall**: `target_total / 10`.
    - **Per-dimension**: `target_dim / 10`.

Run directly with Python (example):

```bash
python -u deepresearch_bench_race.py claude-opus-tickr-0929 \
  --no_reference \
  --raw_data_dir data/test_data/raw_data \
  --cleaned_data_dir data/test_data/cleaned_data \
  --query_file data/prompt_data/query.jsonl \
  --output_dir results/race/claude-opus-3.1-0929-tickr

python -u deepresearch_bench_race.py claude-opus-web-0929 \
  --no_reference \
  --raw_data_dir data/test_data/raw_data \
  --cleaned_data_dir data/test_data/cleaned_data \
  --query_file data/prompt_data/query.jsonl \
  --output_dir results/race/claude-opus-3.1-0929-web
```

Tip: You can also add `--no_reference` to the Python command inside `run_benchmark.sh` if you prefer to use the script.

### Custom LLM Integration

If you're not using the official Gemini API or want to use other LLMs for evaluation, modify the `AIClient` class in `utils/api.py` to implement your custom LLM interface.

## Acknowledgements

We would like to express our gratitude to the following contributors who helped us collect evaluation data. Since many models and agents do not provide public APIs, manual data collection was necessary, and we deeply appreciate their dedicated efforts:

**Xin Yang**, **Jie Yang**, **Yawen Li**, **Xinyu Ouyang**, **Jiaqi He**, **Gefan Zhang**, **Jinfu Liao**, **Qiuyue Chen**, **Yulin Wang**, and **Lina Wang**.

Their contributions were essential to the comprehensive evaluation presented in this benchmark.

## Citation

If you use DeepResearch Bench in your research, please cite our paper:

```bibtex
@article{du2025deepresearch,
  author    = {Mingxuan Du and Benfeng Xu and Chiwei Zhu and Xiaorui Wang and Zhendong Mao},
  title     = {DeepResearch Bench: A Comprehensive Benchmark for Deep Research Agents},
  journal   = {arXiv preprint},
  year      = {2025},
}
``` 