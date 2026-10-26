# Test evidence: issue #34

Verified 2026-10-26 on `fix/34-rate-limit-headers`, implementation commit `aa04f84`, against fetched upstream `main` at `2f4e82f`. No implementation changes were needed in Unit 4.

## Before (authentic Unit 2 baseline, not rerun)

Source: https://github.com/codepath/pathreview-ai301-fa26-s3/issues/34#issuecomment-6242178940 and the preserved Unit 3 plan. On `main` at `2f4e82f`, the single root request returned HTTP 200 with no rate-limit headers. The 200-request root burst returned `200 200`; the health burst returned `200 503`; 50 wrong-password login attempts returned `50 401`. The in-process trace reported `check_rate_limit calls observed: 0`.

## After (actual Unit 4 rerun)

The existing virtual environment, `.env`, seeded database and Docker services were reused. The test API ran on `127.0.0.1:8010`, because an unrelated application occupied 8000. Cleared only the local reproduction identifier keys between phases; no database flush. API used `LLM_PROVIDER=mock`. The commands and output below were captured from subprocesses, not predicted.

- Single root request: HTTP 200, `X-RateLimit-Limit: 60`, `X-RateLimit-Remaining: 59`.
- Fresh root burst: 60 HTTP 200, 140 HTTP 429. Additional denied sample: remaining 0 and `Retry-After: 60`.
- Health control: 200 HTTP 503, unchanged. Its existing SQLAlchemy `SELECT 1` and nonexistent `settings.redis_host` problems remain outside this change.
- Wrong-password login burst: 50 HTTP 401. The additional sample, request 51 in that window, reported remaining 9.
- Original posted trace script: root 20 HTTP 200, health 20 HTTP 503, sample remaining 39, and 21 limiter calls.
- Static search finds the live middleware caller at `api/middleware/rate_limit.py:69`.

## Prescribed checks

| Command | Actual result | Exit |
|---|---|---|
| `make test-unit` | 385 passed, 53 xfailed, 3 warnings | 0 |
| `make test-integration` | 6 passed, 4 deprecation warnings; real Redis, including concurrency | 0 |
| `make lint` | All checks passed | 0 |
| `make typecheck` | Success: no issues found in 77 source files | 0 |

The 53 xfails are unrelated seeded bugs. Search of tests and pyproject.toml found no issue #34 xfail or suppression to remove. `git diff upstream/main...HEAD --check` passed. Black reported 114 files unchanged. Frontend initially had one timeout under concurrent load (17 passed, 1 failed); the same `npm test -- --run` command rerun alone passed 18/18 without edits. These are separate runs, not a hidden first failure.

## Limitations

Per-IP identity shares quota behind proxies. Redis failures still fail open and report the full configured quota. `/health` and OPTIONS are exempt; no claim that every response carries headers. Retry-After is a 60-second bound. The mock-script unit tests cannot independently validate Lua; six integration tests cover the real Redis implementation. CI status is recorded in the PR and Unit 4 write-up separately.

## Captured four-check output

### test-unit

```text
$ make test-unit
.venv/bin/pytest tests/unit -v -m unit
============================= test session starts ==============================
platform darwin -- Python 3.11.15, pytest-9.1.1, pluggy-1.7.0 -- /Users/aryahb/Downloads/pathreview-ai301-fa26-s3/.venv/bin/python
cachedir: .pytest_cache
hypothesis profile 'default'
benchmark: 5.3.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /Users/aryahb/Downloads/pathreview-ai301-fa26-s3
configfile: pyproject.toml
plugins: pytest_httpserver-1.2.0, hypothesis-6.170.1, cov-7.1.0, asyncio-1.4.0, benchmark-5.3.0, platformdirs-4.13.4, anyio-4.15.1
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 438 items

tests/unit/test_batch_processor.py::TestBatchEmbeddingProcessor::test_empty_chunks_list_returns_empty XFAIL [  0%]
tests/unit/test_batch_processor.py::TestBatchEmbeddingProcessor::test_normal_chunks_list_processes PASSED [  0%]
tests/unit/test_batch_processor.py::TestBatchEmbeddingProcessor::test_batches_chunks_correctly PASSED [  0%]
tests/unit/test_batch_processor.py::TestBatchEmbeddingProcessor::test_returns_chunk_and_embedding_id_tuples PASSED [  0%]
tests/unit/test_batch_processor.py::TestBatchEmbeddingProcessor::test_embedding_provider_called_with_texts PASSED [  1%]
tests/unit/test_batch_processor.py::TestBatchEmbeddingProcessor::test_chunk_metadata_preserved PASSED [  1%]
tests/unit/test_batch_processor.py::TestBatchEmbeddingProcessor::test_batch_size_limit PASSED [  1%]
tests/unit/test_batch_processor.py::TestBatchEmbeddingProcessor::test_many_chunks PASSED [  1%]
tests/unit/test_batch_processor.py::TestBatchEmbeddingProcessor::test_embedding_provider_exception_propagates PASSED [  2%]
tests/unit/test_batch_processor.py::TestBatchEmbeddingProcessor::test_store_embedding_called_for_each_chunk PASSED [  2%]
tests/unit/test_batch_processor.py::TestBatchEmbeddingProcessor::test_chunk_text_extraction PASSED [  2%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_dismissive_bootcamp_language_detected XFAIL [  2%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_bootcamp_lacks_rigor_detected XFAIL [  2%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_bootcamp_inadequate_training_detected PASSED [  3%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_self_taught_comparison_detected PASSED [  3%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_positive_bootcamp_mention_not_flagged PASSED [  3%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_neutral_bootcamp_mention_not_flagged PASSED [  3%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_educational_background_positive_not_flagged PASSED [  4%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_demographic_assumption_age_detected XFAIL [  4%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_demographic_assumption_old_detected PASSED [  4%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_demographic_assumption_background_detected PASSED [  4%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_immigrant_developer_assumption_detected PASSED [  5%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_international_developer_assumption_detected PASSED [  5%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_clean_feedback_not_flagged PASSED [  5%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_technical_feedback_not_flagged PASSED [  5%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_development_suggestion_not_flagged PASSED [  5%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_case_insensitive_detection PASSED [  6%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_return_value_structure PASSED [  6%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_unbiased_returns_empty_reason PASSED [  6%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_biased_returns_reason PASSED [  6%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_empty_text PASSED [  7%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_whitespace_only PASSED [  7%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_coding_bootcamp_variant XFAIL [  7%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_online_course_bias_detected PASSED [  7%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_developer_vs_programmer_distinction XFAIL [  7%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_multiple_bias_indicators XFAIL [  8%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_negative_educational_claim XFAIL [  8%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_working_class_assumption PASSED [  8%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_rich_poor_assumption XFAIL [  8%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_foreign_developer_struggle_assumption PASSED [  9%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_skill_assessment_not_biased PASSED [  9%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_comparative_without_bias PASSED [  9%]
tests/unit/test_bias_detector.py::TestBiasDetector::test_assumption_vs_observation XFAIL [  9%]
tests/unit/test_faithfulness_checker.py::TestFaithfulnessChecker::test_feedback_fully_supported_by_context PASSED [ 10%]
tests/unit/test_faithfulness_checker.py::TestFaithfulnessChecker::test_feedback_with_no_support_in_context PASSED [ 10%]
tests/unit/test_faithfulness_checker.py::TestFaithfulnessChecker::test_partial_support_returns_middle_score XFAIL [ 10%]
tests/unit/test_faithfulness_checker.py::TestFaithfulnessChecker::test_empty_feedback_returns_zero PASSED [ 10%]
tests/unit/test_faithfulness_checker.py::TestFaithfulnessChecker::test_empty_context_chunks_returns_zero PASSED [ 10%]
tests/unit/test_faithfulness_checker.py::TestFaithfulnessChecker::test_both_empty_returns_zero PASSED [ 11%]
tests/unit/test_faithfulness_checker.py::TestFaithfulnessChecker::test_multiple_context_chunks XFAIL [ 11%]
tests/unit/test_faithfulness_checker.py::TestFaithfulnessChecker::test_extract_claims PASSED [ 11%]
tests/unit/test_faithfulness_checker.py::TestFaithfulnessChecker::test_extract_claims_with_punctuation PASSED [ 11%]
tests/unit/test_faithfulness_checker.py::TestFaithfulnessChecker::test_is_supported_with_keyword_overlap PASSED [ 12%]
tests/unit/test_faithfulness_checker.py::TestFaithfulnessChecker::test_is_supported_without_keywords PASSED [ 12%]
tests/unit/test_faithfulness_checker.py::TestFaithfulnessChecker::test_case_insensitive_support_check PASSED [ 12%]
tests/unit/test_faithfulness_checker.py::TestFaithfulnessChecker::test_score_never_returns_hardcoded_value PASSED [ 12%]
tests/unit/test_faithfulness_checker.py::TestFaithfulnessChecker::test_multiple_claims_varying_support XFAIL [ 13%]
tests/unit/test_faithfulness_checker.py::TestFaithfulnessChecker::test_very_long_feedback PASSED [ 13%]
tests/unit/test_faithfulness_checker.py::TestFaithfulnessChecker::test_very_long_context PASSED [ 13%]
tests/unit/test_faithfulness_checker.py::TestFaithfulnessChecker::test_common_words_filtered_in_overlap PASSED [ 13%]
tests/unit/test_faithfulness_checker.py::TestFaithfulnessChecker::test_minimum_overlap_required PASSED [ 13%]
tests/unit/test_faithfulness_checker.py::TestFaithfulnessChecker::test_none_context_chunk_text XFAIL [ 14%]
tests/unit/test_faithfulness_checker.py::TestFaithfulnessChecker::test_missing_text_key_in_chunk PASSED [ 14%]
tests/unit/test_faithfulness_checker.py::TestFaithfulnessChecker::test_score_consistency PASSED [ 14%]
tests/unit/test_faithfulness_checker.py::TestFaithfulnessChecker::test_specialized_technical_terms PASSED [ 14%]
tests/unit/test_keyword_search.py::TestKeywordSearcher::test_results_sorted_by_score_descending PASSED [ 15%]
tests/unit/test_keyword_search.py::TestKeywordSearcher::test_query_matching_no_documents PASSED [ 15%]
tests/unit/test_keyword_search.py::TestKeywordSearcher::test_query_matching_multiple_documents PASSED [ 15%]
tests/unit/test_keyword_search.py::TestKeywordSearcher::test_case_insensitive_matching PASSED [ 15%]
tests/unit/test_keyword_search.py::TestKeywordSearcher::test_top_k_limit PASSED [ 15%]
tests/unit/test_keyword_search.py::TestKeywordSearcher::test_top_k_larger_than_results PASSED [ 16%]
tests/unit/test_keyword_search.py::TestKeywordSearcher::test_results_have_bm25_score PASSED [ 16%]
tests/unit/test_keyword_search.py::TestKeywordSearcher::test_results_preserve_chunk_fields PASSED [ 16%]
tests/unit/test_keyword_search.py::TestKeywordSearcher::test_empty_index XFAIL [ 16%]
tests/unit/test_keyword_search.py::TestKeywordSearcher::test_index_not_called_returns_empty PASSED [ 17%]
tests/unit/test_keyword_search.py::TestKeywordSearcher::test_multi_word_query PASSED [ 17%]
tests/unit/test_keyword_search.py::TestKeywordSearcher::test_tokenization PASSED [ 17%]
tests/unit/test_keyword_search.py::TestKeywordSearcher::test_tokenization_case_handling PASSED [ 17%]
tests/unit/test_keyword_search.py::TestKeywordSearcher::test_large_corpus PASSED [ 18%]
tests/unit/test_keyword_search.py::TestKeywordSearcher::test_special_characters_in_query PASSED [ 18%]
tests/unit/test_keyword_search.py::TestKeywordSearcher::test_exact_phrase_matching PASSED [ 18%]
tests/unit/test_keyword_search.py::TestKeywordSearcher::test_single_word_chunks PASSED [ 18%]
tests/unit/test_llm_provider_contract.py::TestLLMProviderContract::test_mock_provider_returns_list_of_floats PASSED [ 18%]
tests/unit/test_llm_provider_contract.py::TestLLMProviderContract::test_openai_provider_would_return_floats PASSED [ 19%]
tests/unit/test_llm_provider_contract.py::TestLLMProviderContract::test_mock_provider_deterministic PASSED [ 19%]
tests/unit/test_llm_provider_contract.py::TestLLMProviderContract::test_mock_provider_embedding_dimension PASSED [ 19%]
tests/unit/test_llm_provider_contract.py::TestLLMProviderContract::test_providers_same_dimension PASSED [ 19%]
tests/unit/test_llm_provider_contract.py::TestLLMProviderContract::test_mock_provider_multiple_texts PASSED [ 20%]
tests/unit/test_llm_provider_contract.py::TestLLMProviderContract::test_mock_provider_empty_list PASSED [ 20%]
tests/unit/test_llm_provider_contract.py::TestLLMProviderContract::test_mock_provider_single_text PASSED [ 20%]
tests/unit/test_llm_provider_contract.py::TestLLMProviderContract::test_mock_provider_empty_string PASSED [ 20%]
tests/unit/test_llm_provider_contract.py::TestLLMProviderContract::test_mock_provider_different_inputs_different_outputs PASSED [ 21%]
tests/unit/test_llm_provider_contract.py::TestLLMProviderContract::test_mock_provider_embeddings_normalized PASSED [ 21%]
tests/unit/test_llm_provider_contract.py::TestLLMProviderContract::test_provider_interface_implements_embed PASSED [ 21%]
tests/unit/test_llm_provider_contract.py::TestLLMProviderContract::test_mock_provider_returns_floats_not_integers PASSED [ 21%]
tests/unit/test_llm_provider_contract.py::TestLLMProviderContract::test_multiple_providers_same_interface PASSED [ 21%]
tests/unit/test_llm_provider_contract.py::TestLLMProviderContract::test_mock_provider_consistency_across_calls PASSED [ 22%]
tests/unit/test_llm_provider_contract.py::TestLLMProviderContract::test_provider_embed_signature PASSED [ 22%]
tests/unit/test_llm_provider_contract.py::TestLLMProviderContract::test_mock_provider_with_very_long_text PASSED [ 22%]
tests/unit/test_llm_provider_contract.py::TestLLMProviderContract::test_mock_provider_with_special_characters PASSED [ 22%]
tests/unit/test_llm_provider_contract.py::TestLLMProviderContract::test_mock_provider_with_unicode PASSED [ 23%]
tests/unit/test_llm_provider_contract.py::TestLLMProviderContract::test_mock_provider_with_newlines PASSED [ 23%]
tests/unit/test_llm_provider_contract.py::TestLLMProviderContract::test_mock_provider_with_tabs PASSED [ 23%]
tests/unit/test_llm_provider_contract.py::TestLLMProviderContract::test_different_text_lengths_same_output_dimension PASSED [ 23%]
tests/unit/test_llm_provider_contract.py::TestLLMProviderContract::test_mock_provider_batch_processing PASSED [ 23%]
tests/unit/test_llm_provider_contract.py::TestLLMProviderContract::test_embedding_vector_values_in_valid_range PASSED [ 24%]
tests/unit/test_llm_provider_contract.py::TestLLMProviderContract::test_providers_inherit_from_abstract_base PASSED [ 24%]
tests/unit/test_llm_provider_contract.py::TestLLMProviderContract::test_abstract_base_class_has_embed_method PASSED [ 24%]
tests/unit/test_llm_provider_contract.py::TestLLMProviderContract::test_mock_provider_embedding_stability PASSED [ 24%]
tests/unit/test_output_parser.py::TestOutputParser::test_json_wrapped_in_code_fence PASSED [ 25%]
tests/unit/test_output_parser.py::TestOutputParser::test_raw_json_without_fence PASSED [ 25%]
tests/unit/test_output_parser.py::TestOutputParser::test_plain_text_fallback PASSED [ 25%]
tests/unit/test_output_parser.py::TestOutputParser::test_malformed_json_fallback PASSED [ 25%]
tests/unit/test_output_parser.py::TestOutputParser::test_feedback_section_has_required_fields PASSED [ 26%]
tests/unit/test_output_parser.py::TestOutputParser::test_json_with_multiple_sections PASSED [ 26%]
tests/unit/test_output_parser.py::TestOutputParser::test_confidence_scores_in_sections PASSED [ 26%]
tests/unit/test_output_parser.py::TestOutputParser::test_empty_json_object PASSED [ 26%]
tests/unit/test_output_parser.py::TestOutputParser::test_json_array_fallback XFAIL [ 26%]
tests/unit/test_output_parser.py::TestOutputParser::test_very_long_plain_text PASSED [ 27%]
tests/unit/test_output_parser.py::TestOutputParser::test_html_in_feedback PASSED [ 27%]
tests/unit/test_output_parser.py::TestOutputParser::test_code_in_feedback PASSED [ 27%]
tests/unit/test_output_parser.py::TestOutputParser::test_section_suggestions_extraction PASSED [ 27%]
tests/unit/test_output_parser.py::TestOutputParser::test_unicode_characters PASSED [ 28%]
tests/unit/test_output_parser.py::TestOutputParser::test_nested_json_structure PASSED [ 28%]
tests/unit/test_output_parser.py::TestOutputParser::test_mixed_content PASSED [ 28%]
tests/unit/test_output_parser.py::TestOutputParser::test_plaintext_output_helper PASSED [ 28%]
tests/unit/test_output_parser.py::TestOutputParser::test_multiple_code_fences PASSED [ 28%]
tests/unit/test_output_parser.py::TestOutputParser::test_no_suggestions_key PASSED [ 29%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_email_redaction PASSED [ 29%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_multiple_emails_redacted PASSED [ 29%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_us_phone_number_redaction XFAIL [ 29%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_us_phone_formats XFAIL [ 30%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_international_phone_redaction PASSED [ 30%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_ssn_redaction PASSED [ 30%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_ssn_variations PASSED [ 30%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_street_address_redaction PASSED [ 31%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_text_with_no_pii PASSED [ 31%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_detect_returns_list_of_pii PASSED [ 31%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_detect_email_pii PASSED [ 31%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_detect_phone_pii XFAIL [ 31%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_detect_ssn_pii PASSED [ 32%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_detect_positions_accurate PASSED [ 32%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_detect_multiple_pii_items PASSED [ 32%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_case_insensitive_email_matching PASSED [ 32%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_complex_email_addresses PASSED [ 33%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_phone_at_start_of_text XFAIL [ 33%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_phone_at_end_of_text PASSED [ 33%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_address_variations PASSED [ 33%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_empty_text PASSED [ 34%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_whitespace_only PASSED [ 34%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_mixed_pii_and_text XFAIL [ 34%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_scrub_idempotent PASSED [ 34%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_detect_no_false_positives PASSED [ 34%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_newline_injection_detected PASSED [ 35%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_system_role_switching_detected PASSED [ 35%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_human_role_switching_detected PASSED [ 35%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_assistant_role_switching_detected PASSED [ 35%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_template_injection_detected PASSED [ 36%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_jinja_injection_detected PASSED [ 36%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_ignore_instruction_detected PASSED [ 36%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_forget_instruction_detected PASSED [ 36%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_disregard_instruction_detected PASSED [ 36%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_override_instruction_detected PASSED [ 37%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_code_execution_attempt_detected PASSED [ 37%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_run_function_attempt_detected PASSED [ 37%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_eval_function_attempt_detected PASSED [ 37%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_clean_input_not_flagged PASSED [ 38%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_normal_text_not_flagged PASSED [ 38%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_sanitize_removes_template_delimiters PASSED [ 38%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_sanitize_removes_angle_brackets PASSED [ 38%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_sanitize_preserves_legitimate_content PASSED [ 39%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_sanitize_multiple_template_delimiters PASSED [ 39%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_separator_line_detected PASSED [ 39%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_long_separator_detected PASSED [ 39%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_case_insensitive_detection PASSED [ 39%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_whitespace_variations_detected XFAIL [ 40%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_multiple_injection_patterns PASSED [ 40%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_benign_mentions_not_flagged PASSED [ 40%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_empty_string PASSED [ 40%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_whitespace_only PASSED [ 41%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_sanitize_idempotent PASSED [ 41%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_complex_injection_attempt PASSED [ 41%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_legitimate_newlines_not_flagged PASSED [ 41%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_code_blocks_handled PASSED [ 42%]
tests/unit/test_prompt_defense.py::TestPromptDefense::test_sanitize_with_mixed_delimiters PASSED [ 42%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_all_5_templates_exist PASSED [ 42%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_skills_feedback_template_exists PASSED [ 42%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_projects_feedback_template_exists PASSED [ 42%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_presentation_feedback_template_exists PASSED [ 43%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_gaps_feedback_template_exists PASSED [ 43%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_first_impression_template_exists PASSED [ 43%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_each_template_contains_context_placeholder PASSED [ 43%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_each_template_contains_github_username_placeholder PASSED [ 44%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_each_template_contains_project_count_placeholder PASSED [ 44%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_get_template_returns_correct_template PASSED [ 44%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_get_template_projects_feedback PASSED [ 44%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_get_template_presentation_feedback PASSED [ 44%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_get_template_gaps_feedback PASSED [ 45%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_get_template_first_impression PASSED [ 45%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_get_template_unknown_name_raises_error PASSED [ 45%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_get_template_unknown_version_raises_error PASSED [ 45%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_all_templates_have_v1 PASSED [ 46%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_templates_are_strings PASSED [ 46%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_templates_have_reasonable_length PASSED [ 46%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_skills_feedback_mentions_technical_skills PASSED [ 46%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_projects_feedback_mentions_code_quality PASSED [ 47%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_gaps_feedback_mentions_missing_skills PASSED [ 47%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_presentation_feedback_mentions_readme PASSED [ 47%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_first_impression_is_concise PASSED [ 47%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_get_template_default_version PASSED [ 47%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_template_snapshot_content_hash PASSED [ 48%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_skills_feedback_requests_json_format PASSED [ 48%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_projects_feedback_requests_json_format PASSED [ 48%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_presentation_feedback_requests_json_format PASSED [ 48%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_gaps_feedback_requests_json_format PASSED [ 49%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_first_impression_plain_text PASSED [ 49%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_templates_have_portfolio_context PASSED [ 49%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_template_get_logs_retrieval PASSED [ 49%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_each_template_name_is_valid_identifier PASSED [ 50%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_template_versions_are_strings PASSED [ 50%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_no_hardcoded_usernames_in_templates PASSED [ 50%]
tests/unit/test_prompt_templates.py::TestPromptTemplates::test_templates_use_consistent_placeholders PASSED [ 50%]
tests/unit/test_rate_limit_middleware.py::TestRateLimitMiddleware::test_allowed_request_has_rate_limit_headers PASSED [ 50%]
tests/unit/test_rate_limit_middleware.py::TestRateLimitMiddleware::test_denied_request_returns_429_with_retry_after PASSED [ 51%]
tests/unit/test_rate_limit_middleware.py::TestRateLimitMiddleware::test_health_is_exempt_from_limiting PASSED [ 51%]
tests/unit/test_rate_limit_middleware.py::TestRateLimitMiddleware::test_options_requests_are_not_limited PASSED [ 51%]
tests/unit/test_rate_limit_middleware.py::TestRateLimitMiddleware::test_identifier_is_client_host PASSED [ 51%]
tests/unit/test_rate_limit_middleware.py::TestRateLimitMiddleware::test_remaining_value_comes_from_limiter[59] PASSED [ 52%]
tests/unit/test_rate_limit_middleware.py::TestRateLimitMiddleware::test_remaining_value_comes_from_limiter[30] PASSED [ 52%]
tests/unit/test_rate_limit_middleware.py::TestRateLimitMiddleware::test_remaining_value_comes_from_limiter[0] PASSED [ 52%]
tests/unit/test_rate_limit_middleware.py::TestRateLimitMiddleware::test_fail_open_reports_limit_as_remaining PASSED [ 52%]
tests/unit/test_rate_limiter.py::TestRateLimiter::test_first_request_allowed PASSED [ 52%]
tests/unit/test_rate_limiter.py::TestRateLimiter::test_requests_up_to_limit_allowed PASSED [ 53%]
tests/unit/test_rate_limiter.py::TestRateLimiter::test_request_at_limit_plus_one_denied PASSED [ 53%]
tests/unit/test_rate_limiter.py::TestRateLimiter::test_remaining_count_correct PASSED [ 53%]
tests/unit/test_rate_limiter.py::TestRateLimiter::test_rolling_window_removes_old_entries PASSED [ 53%]
tests/unit/test_rate_limiter.py::TestRateLimiter::test_different_identifiers_independent PASSED [ 54%]
tests/unit/test_rate_limiter.py::TestRateLimiter::test_key_format_correct PASSED [ 54%]
tests/unit/test_rate_limiter.py::TestRateLimiter::test_entry_added_to_redis PASSED [ 54%]
tests/unit/test_rate_limiter.py::TestRateLimiter::test_expiry_set_correctly PASSED [ 54%]
tests/unit/test_rate_limiter.py::TestRateLimiter::test_custom_window_size PASSED [ 55%]
tests/unit/test_rate_limiter.py::TestRateLimiter::test_redis_error_handling PASSED [ 55%]
tests/unit/test_rate_limiter.py::TestRateLimiter::test_zero_limit PASSED [ 55%]
tests/unit/test_rate_limiter.py::TestRateLimiter::test_negative_limit PASSED [ 55%]
tests/unit/test_rate_limiter.py::TestRateLimiter::test_large_limit PASSED [ 55%]
tests/unit/test_rate_limiter.py::TestRateLimiter::test_return_tuple_structure PASSED [ 56%]
tests/unit/test_rate_limiter.py::TestRateLimiter::test_multiple_requests_same_user PASSED [ 56%]
tests/unit/test_rate_limiter.py::TestRateLimiter::test_time_based_window_calculation PASSED [ 56%]
tests/unit/test_rate_limiter.py::TestRateLimiter::test_ip_address_as_identifier PASSED [ 56%]
tests/unit/test_rate_limiter.py::TestRateLimiter::test_api_key_as_identifier PASSED [ 57%]
tests/unit/test_rate_limiter.py::TestRateLimiter::test_requests_at_same_timestamp_get_unique_members PASSED [ 57%]
tests/unit/test_readme_parser.py::TestReadmeParser::test_parse_standard_readme XFAIL [ 57%]
tests/unit/test_readme_parser.py::TestReadmeParser::test_parse_readme_longer_than_10000_chars PASSED [ 57%]
tests/unit/test_readme_parser.py::TestReadmeParser::test_parse_readme_with_code_blocks PASSED [ 57%]
tests/unit/test_readme_parser.py::TestReadmeParser::test_parse_readme_without_code_blocks PASSED [ 58%]
tests/unit/test_readme_parser.py::TestReadmeParser::test_parse_empty_readme PASSED [ 58%]
tests/unit/test_readme_parser.py::TestReadmeParser::test_parse_readme_with_only_whitespace PASSED [ 58%]
tests/unit/test_readme_parser.py::TestReadmeParser::test_parse_readme_bytes_input PASSED [ 58%]
tests/unit/test_readme_parser.py::TestReadmeParser::test_parse_readme_bytes_with_utf8 PASSED [ 59%]
tests/unit/test_readme_parser.py::TestReadmeParser::test_parse_invalid_content_type PASSED [ 59%]
tests/unit/test_readme_parser.py::TestReadmeParser::test_extract_heading_hierarchy XFAIL [ 59%]
tests/unit/test_readme_parser.py::TestReadmeParser::test_extract_heading_hierarchy_no_headings PASSED [ 59%]
tests/unit/test_readme_parser.py::TestReadmeParser::test_parse_readme_with_badges PASSED [ 60%]
tests/unit/test_readme_parser.py::TestReadmeParser::test_parse_readme_without_badges PASSED [ 60%]
tests/unit/test_readme_parser.py::TestReadmeParser::test_metadata_structure PASSED [ 60%]
tests/unit/test_readme_parser.py::TestReadmeParser::test_word_count_accuracy PASSED [ 60%]
tests/unit/test_readme_scorer.py::TestReadmeScorer::test_readme_with_all_quality_signals XFAIL [ 60%]
tests/unit/test_readme_scorer.py::TestReadmeScorer::test_readme_with_no_content PASSED [ 61%]
tests/unit/test_readme_scorer.py::TestReadmeScorer::test_readme_with_only_title PASSED [ 61%]
tests/unit/test_readme_scorer.py::TestReadmeScorer::test_word_count_category_minimal PASSED [ 61%]
tests/unit/test_readme_scorer.py::TestReadmeScorer::test_word_count_category_adequate PASSED [ 61%]
tests/unit/test_readme_scorer.py::TestReadmeScorer::test_word_count_category_comprehensive PASSED [ 62%]
tests/unit/test_readme_scorer.py::TestReadmeScorer::test_installation_section_detection PASSED [ 62%]
tests/unit/test_readme_scorer.py::TestReadmeScorer::test_usage_section_detection PASSED [ 62%]
tests/unit/test_readme_scorer.py::TestReadmeScorer::test_setup_keyword_counts_as_installation PASSED [ 62%]
tests/unit/test_readme_scorer.py::TestReadmeScorer::test_quickstart_counts_as_usage PASSED [ 63%]
tests/unit/test_readme_scorer.py::TestReadmeScorer::test_badge_detection PASSED [ 63%]
tests/unit/test_readme_scorer.py::TestReadmeScorer::test_demo_link_detection PASSED [ 63%]
tests/unit/test_readme_scorer.py::TestReadmeScorer::test_tech_stack_section_detection PASSED [ 63%]
tests/unit/test_readme_scorer.py::TestReadmeScorer::test_technologies_keyword_counts PASSED [ 63%]
tests/unit/test_readme_scorer.py::TestReadmeScorer::test_overall_score_calculation PASSED [ 64%]
tests/unit/test_readme_scorer.py::TestReadmeScorer::test_missing_readme_content_key PASSED [ 64%]
tests/unit/test_readme_scorer.py::TestReadmeScorer::test_result_has_all_required_fields PASSED [ 64%]
tests/unit/test_readme_scorer.py::TestReadmeScorer::test_case_insensitive_section_detection PASSED [ 64%]
tests/unit/test_readme_scorer.py::TestReadmeScorer::test_whitespace_only_readme PASSED [ 65%]
tests/unit/test_readme_scorer.py::TestReadmeScorer::test_example_keyword_counts_as_usage PASSED [ 65%]
tests/unit/test_readme_scorer.py::TestReadmeScorer::test_score_scales_with_word_count PASSED [ 65%]
tests/unit/test_readme_scorer.py::TestReadmeScorer::test_try_it_as_demo_indicator PASSED [ 65%]
tests/unit/test_readme_scorer.py::TestReadmeScorer::test_built_with_counts_as_tech_stack PASSED [ 65%]
tests/unit/test_relevance_scorer.py::TestRelevanceScorer::test_query_with_perfect_keyword_match PASSED [ 66%]
tests/unit/test_relevance_scorer.py::TestRelevanceScorer::test_query_with_zero_keyword_overlap PASSED [ 66%]
tests/unit/test_relevance_scorer.py::TestRelevanceScorer::test_query_with_partial_overlap XFAIL [ 66%]
tests/unit/test_relevance_scorer.py::TestRelevanceScorer::test_empty_chunks_list_returns_zero PASSED [ 66%]
tests/unit/test_relevance_scorer.py::TestRelevanceScorer::test_empty_query_returns_zero PASSED [ 67%]
tests/unit/test_relevance_scorer.py::TestRelevanceScorer::test_multiple_chunks_aggregated PASSED [ 67%]
tests/unit/test_relevance_scorer.py::TestRelevanceScorer::test_case_insensitive_matching PASSED [ 67%]
tests/unit/test_relevance_scorer.py::TestRelevanceScorer::test_tokenization PASSED [ 67%]
tests/unit/test_relevance_scorer.py::TestRelevanceScorer::test_empty_text_in_chunk PASSED [ 68%]
tests/unit/test_relevance_scorer.py::TestRelevanceScorer::test_very_long_query PASSED [ 68%]
tests/unit/test_relevance_scorer.py::TestRelevanceScorer::test_very_long_chunk PASSED [ 68%]
tests/unit/test_relevance_scorer.py::TestRelevanceScorer::test_special_characters_ignored PASSED [ 68%]
tests/unit/test_relevance_scorer.py::TestRelevanceScorer::test_multiple_keyword_matches PASSED [ 68%]
tests/unit/test_relevance_scorer.py::TestRelevanceScorer::test_single_word_chunks PASSED [ 69%]
tests/unit/test_relevance_scorer.py::TestRelevanceScorer::test_score_ranges_from_zero_to_one PASSED [ 69%]
tests/unit/test_relevance_scorer.py::TestRelevanceScorer::test_common_words_not_preventing_scoring PASSED [ 69%]
tests/unit/test_relevance_scorer.py::TestRelevanceScorer::test_chunk_without_text_key PASSED [ 69%]
tests/unit/test_relevance_scorer.py::TestRelevanceScorer::test_whitespace_only_in_chunks PASSED [ 70%]
tests/unit/test_relevance_scorer.py::TestRelevanceScorer::test_average_relevance_calculation PASSED [ 70%]
tests/unit/test_resume_parser.py::TestResumeParser::test_parse_single_column_resume_text XFAIL [ 70%]
tests/unit/test_resume_parser.py::TestResumeParser::test_parse_resume_no_work_experience XFAIL [ 70%]
tests/unit/test_resume_parser.py::TestResumeParser::test_parse_multipage_pdf PASSED [ 71%]
tests/unit/test_resume_parser.py::TestResumeParser::test_parse_markdown_resume XFAIL [ 71%]
tests/unit/test_resume_parser.py::TestResumeParser::test_parse_invalid_content_type PASSED [ 71%]
tests/unit/test_resume_parser.py::TestResumeParser::test_parse_invalid_list_content PASSED [ 71%]
tests/unit/test_resume_parser.py::TestResumeParser::test_detect_sections XFAIL [ 71%]
tests/unit/test_resume_parser.py::TestResumeParser::test_strip_markdown_syntax XFAIL [ 72%]
tests/unit/test_resume_parser.py::TestResumeParser::test_pdf_parsing_error_handling PASSED [ 72%]
tests/unit/test_resume_parser.py::TestResumeParser::test_parse_preserves_text_content PASSED [ 72%]
tests/unit/test_review_service.py::TestReviewService::test_create_review_returns_review_with_pending_status PASSED [ 72%]
tests/unit/test_review_service.py::TestReviewService::test_get_review_returns_review_for_correct_owner XFAIL [ 73%]
tests/unit/test_review_service.py::TestReviewService::test_get_review_returns_none_for_wrong_user XFAIL [ 73%]
tests/unit/test_review_service.py::TestReviewService::test_list_reviews_returns_paginated_results XFAIL [ 73%]
tests/unit/test_review_service.py::TestReviewService::test_list_reviews_page_2_returns_correct_offset XFAIL [ 73%]
tests/unit/test_review_service.py::TestReviewService::test_list_reviews_returns_tuple XFAIL [ 73%]
tests/unit/test_review_service.py::TestReviewService::test_create_review_calls_db_add PASSED [ 74%]
tests/unit/test_review_service.py::TestReviewService::test_create_review_calls_db_commit PASSED [ 74%]
tests/unit/test_review_service.py::TestReviewService::test_create_review_calls_db_refresh PASSED [ 74%]
tests/unit/test_review_service.py::TestReviewService::test_get_review_uses_select_and_join XFAIL [ 74%]
tests/unit/test_review_service.py::TestReviewService::test_list_reviews_default_pagination XFAIL [ 75%]
tests/unit/test_review_service.py::TestReviewService::test_list_reviews_custom_page_size XFAIL [ 75%]
tests/unit/test_review_service.py::TestReviewService::test_create_review_with_uuid_ids PASSED [ 75%]
tests/unit/test_review_service.py::TestReviewService::test_get_review_verifies_ownership XFAIL [ 75%]
tests/unit/test_review_service.py::TestReviewService::test_list_reviews_counts_total XFAIL [ 76%]
tests/unit/test_review_service.py::TestReviewService::test_list_reviews_returns_reviews_list XFAIL [ 76%]
tests/unit/test_review_service.py::TestReviewService::test_review_sections_and_score_initially_none PASSED [ 76%]
tests/unit/test_review_service.py::TestReviewService::test_get_review_with_valid_uuid XFAIL [ 76%]
tests/unit/test_review_service.py::TestReviewService::test_list_reviews_ordered_by_created_at XFAIL [ 76%]
tests/unit/test_security.py::TestSecurity::test_hash_password_returns_bcrypt_hash PASSED [ 77%]
tests/unit/test_security.py::TestSecurity::test_verify_password_correct PASSED [ 77%]
tests/unit/test_security.py::TestSecurity::test_verify_password_incorrect PASSED [ 77%]
tests/unit/test_security.py::TestSecurity::test_verify_password_case_sensitive PASSED [ 77%]
tests/unit/test_security.py::TestSecurity::test_hash_same_password_different_hash PASSED [ 78%]
tests/unit/test_security.py::TestSecurity::test_create_access_token_returns_string PASSED [ 78%]
tests/unit/test_security.py::TestSecurity::test_create_access_token_is_jwt PASSED [ 78%]
tests/unit/test_security.py::TestSecurity::test_decode_access_token_valid PASSED [ 78%]
tests/unit/test_security.py::TestSecurity::test_decode_access_token_invalid_token PASSED [ 78%]
tests/unit/test_security.py::TestSecurity::test_decode_access_token_malformed PASSED [ 79%]
tests/unit/test_security.py::TestSecurity::test_decode_access_token_empty_string PASSED [ 79%]
tests/unit/test_security.py::TestSecurity::test_roundtrip_token_with_data PASSED [ 79%]
tests/unit/test_security.py::TestSecurity::test_create_access_token_with_custom_expiry PASSED [ 79%]
tests/unit/test_security.py::TestSecurity::test_access_token_includes_expiration PASSED [ 80%]
tests/unit/test_security.py::TestSecurity::test_password_hash_different_for_different_passwords PASSED [ 80%]
tests/unit/test_security.py::TestSecurity::test_verify_password_with_empty_strings PASSED [ 80%]
tests/unit/test_security.py::TestSecurity::test_verify_password_with_special_characters PASSED [ 80%]
tests/unit/test_security.py::TestSecurity::test_token_with_empty_data PASSED [ 81%]
tests/unit/test_security.py::TestSecurity::test_token_with_special_characters_in_data PASSED [ 81%]
tests/unit/test_security.py::TestSecurity::test_token_with_unicode_data PASSED [ 81%]
tests/unit/test_security.py::TestSecurity::test_hash_password_long_input PASSED [ 81%]
tests/unit/test_security.py::TestSecurity::test_verify_with_wrong_hash_format XFAIL [ 81%]
tests/unit/test_security.py::TestSecurity::test_token_tampering_detection PASSED [ 82%]
tests/unit/test_security.py::TestSecurity::test_create_token_consistency PASSED [ 82%]
tests/unit/test_security.py::TestSecurity::test_password_with_whitespace PASSED [ 82%]
tests/unit/test_semantic_chunker.py::TestSemanticChunker::test_empty_input_returns_empty_list PASSED [ 82%]
tests/unit/test_semantic_chunker.py::TestSemanticChunker::test_whitespace_only_input PASSED [ 83%]
tests/unit/test_semantic_chunker.py::TestSemanticChunker::test_short_text_returns_single_chunk PASSED [ 83%]
tests/unit/test_semantic_chunker.py::TestSemanticChunker::test_long_text_returns_multiple_chunks PASSED [ 83%]
tests/unit/test_semantic_chunker.py::TestSemanticChunker::test_chunk_metadata_includes_chunk_index PASSED [ 83%]
tests/unit/test_semantic_chunker.py::TestSemanticChunker::test_chunks_preserve_source_metadata PASSED [ 84%]
tests/unit/test_semantic_chunker.py::TestSemanticChunker::test_chunk_has_character_positions PASSED [ 84%]
tests/unit/test_semantic_chunker.py::TestSemanticChunker::test_bullet_points_not_split_mid_bullet PASSED [ 84%]
tests/unit/test_semantic_chunker.py::TestSemanticChunker::test_sentence_splitting PASSED [ 84%]
tests/unit/test_semantic_chunker.py::TestSemanticChunker::test_sentence_splitting_with_exclamation_marks PASSED [ 84%]
tests/unit/test_semantic_chunker.py::TestSemanticChunker::test_sentence_splitting_preserves_punctuation PASSED [ 85%]
tests/unit/test_semantic_chunker.py::TestSemanticChunker::test_overlap_between_chunks PASSED [ 85%]
tests/unit/test_semantic_chunker.py::TestSemanticChunker::test_chunks_have_non_zero_text PASSED [ 85%]
tests/unit/test_semantic_chunker.py::TestSemanticChunker::test_paragraph_boundaries_respected PASSED [ 85%]
tests/unit/test_semantic_chunker.py::TestSemanticChunker::test_metadata_copied_not_mutated PASSED [ 86%]
tests/unit/test_semantic_chunker.py::TestSemanticChunker::test_chunk_indexing_is_sequential PASSED [ 86%]
tests/unit/test_skill_extractor.py::TestSkillExtractor::test_text_with_python_imports PASSED [ 86%]
tests/unit/test_skill_extractor.py::TestSkillExtractor::test_text_with_python_type_annotations PASSED [ 86%]
tests/unit/test_skill_extractor.py::TestSkillExtractor::test_text_with_typescript_files XFAIL [ 86%]
tests/unit/test_skill_extractor.py::TestSkillExtractor::test_jupyter_ipynb_detection PASSED [ 87%]
tests/unit/test_skill_extractor.py::TestSkillExtractor::test_mixed_language_text PASSED [ 87%]
tests/unit/test_skill_extractor.py::TestSkillExtractor::test_frameworks_detected_with_high_confidence PASSED [ 87%]
tests/unit/test_skill_extractor.py::TestSkillExtractor::test_react_detection PASSED [ 87%]
tests/unit/test_skill_extractor.py::TestSkillExtractor::test_database_technology_detection XFAIL [ 88%]
tests/unit/test_skill_extractor.py::TestSkillExtractor::test_devops_tool_detection XFAIL [ 88%]
tests/unit/test_skill_extractor.py::TestSkillExtractor::test_skill_has_evidence_list PASSED [ 88%]
tests/unit/test_skill_extractor.py::TestSkillExtractor::test_filename_based_detection PASSED [ 88%]
tests/unit/test_skill_extractor.py::TestSkillExtractor::test_javascript_detection XFAIL [ 89%]
tests/unit/test_skill_extractor.py::TestSkillExtractor::test_docker_compose_detection XFAIL [ 89%]
tests/unit/test_skill_extractor.py::TestSkillExtractor::test_aws_gcp_azure_detection PASSED [ 89%]
tests/unit/test_skill_extractor.py::TestSkillExtractor::test_empty_text PASSED [ 89%]
tests/unit/test_skill_extractor.py::TestSkillExtractor::test_unrecognized_language PASSED [ 89%]
tests/unit/test_skill_extractor.py::TestSkillExtractor::test_confidence_scores_are_floats PASSED [ 90%]
tests/unit/test_skill_extractor.py::TestSkillExtractor::test_skill_detection_dataclass PASSED [ 90%]
tests/unit/test_structural_chunker.py::TestStructuralChunker::test_empty_input_returns_empty_list PASSED [ 90%]
tests/unit/test_structural_chunker.py::TestStructuralChunker::test_whitespace_only_input PASSED [ 90%]
tests/unit/test_structural_chunker.py::TestStructuralChunker::test_document_with_no_headings XFAIL [ 91%]
tests/unit/test_structural_chunker.py::TestStructuralChunker::test_document_with_nested_headings PASSED [ 91%]
tests/unit/test_structural_chunker.py::TestStructuralChunker::test_heading_path_format PASSED [ 91%]
tests/unit/test_structural_chunker.py::TestStructuralChunker::test_large_section_sub_chunked PASSED [ 91%]
tests/unit/test_structural_chunker.py::TestStructuralChunker::test_chunk_metadata_includes_heading_level PASSED [ 92%]
tests/unit/test_structural_chunker.py::TestStructuralChunker::test_chunk_metadata_structure PASSED [ 92%]
tests/unit/test_structural_chunker.py::TestStructuralChunker::test_preserve_source_metadata PASSED [ 92%]
tests/unit/test_structural_chunker.py::TestStructuralChunker::test_multiple_h1_headings PASSED [ 92%]
tests/unit/test_structural_chunker.py::TestStructuralChunker::test_heading_path_breadcrumb PASSED [ 92%]
tests/unit/test_structural_chunker.py::TestStructuralChunker::test_chunks_have_text_content PASSED [ 93%]
tests/unit/test_structural_chunker.py::TestStructuralChunker::test_section_extraction_with_multiple_levels PASSED [ 93%]
tests/unit/test_structural_chunker.py::TestStructuralChunker::test_heading_not_in_middle_of_content PASSED [ 93%]
tests/unit/test_structural_chunker.py::TestStructuralChunker::test_empty_sections_handled PASSED [ 93%]
tests/unit/test_tech_detector.py::TestTechDetector::test_single_language_repo PASSED [ 94%]
tests/unit/test_tech_detector.py::TestTechDetector::test_mixed_language_repo_python_primary PASSED [ 94%]
tests/unit/test_tech_detector.py::TestTechDetector::test_ipynb_counted_as_python_not_json PASSED [ 94%]
tests/unit/test_tech_detector.py::TestTechDetector::test_node_modules_excluded XFAIL [ 94%]
tests/unit/test_tech_detector.py::TestTechDetector::test_vendor_files_excluded PASSED [ 94%]
tests/unit/test_tech_detector.py::TestTechDetector::test_build_directory_excluded XFAIL [ 95%]
tests/unit/test_tech_detector.py::TestTechDetector::test_config_file_detection PASSED [ 95%]
tests/unit/test_tech_detector.py::TestTechDetector::test_dockerfile_detection PASSED [ 95%]
tests/unit/test_tech_detector.py::TestTechDetector::test_github_actions_detection PASSED [ 95%]
tests/unit/test_tech_detector.py::TestTechDetector::test_makefile_detection PASSED [ 96%]
tests/unit/test_tech_detector.py::TestTechDetector::test_typescript_detection PASSED [ 96%]
tests/unit/test_tech_detector.py::TestTechDetector::test_go_detection PASSED [ 96%]
tests/unit/test_tech_detector.py::TestTechDetector::test_rust_detection PASSED [ 96%]
tests/unit/test_tech_detector.py::TestTechDetector::test_java_detection PASSED [ 97%]
tests/unit/test_tech_detector.py::TestTechDetector::test_multiple_python_files PASSED [ 97%]
tests/unit/test_tech_detector.py::TestTechDetector::test_empty_file_list PASSED [ 97%]
tests/unit/test_tech_detector.py::TestTechDetector::test_no_files_key PASSED [ 97%]
tests/unit/test_tech_detector.py::TestTechDetector::test_result_structure PASSED [ 97%]
tests/unit/test_tech_detector.py::TestTechDetector::test_framework_detection PASSED [ 98%]
tests/unit/test_tech_detector.py::TestTechDetector::test_unknown_extensions PASSED [ 98%]
tests/unit/test_tech_detector.py::TestTechDetector::test_case_insensitive_extension_matching PASSED [ 98%]
tests/unit/test_tech_detector.py::TestTechDetector::test_multiple_extensions_same_file PASSED [ 98%]
tests/unit/test_tech_detector.py::TestTechDetector::test_all_languages_sorted PASSED [ 99%]
tests/unit/test_tech_detector.py::TestTechDetector::test_frameworks_sorted PASSED [ 99%]
tests/unit/test_tech_detector.py::TestTechDetector::test_ruby_detection PASSED [ 99%]
tests/unit/test_tech_detector.py::TestTechDetector::test_csharp_detection PASSED [ 99%]
tests/unit/test_tech_detector.py::TestTechDetector::test_cpp_detection PASSED [100%]/Users/aryahb/Downloads/pathreview-ai301-fa26-s3/.venv/lib/python3.11/site-packages/_pytest/unraisableexception.py:33: RuntimeWarning: coroutine 'AsyncMockMixin._execute_mock_call' was never awaited
  gc.collect()
RuntimeWarning: Enable tracemalloc to get the object allocation traceback


=============================== warnings summary ===============================
core/config.py:7
  /Users/aryahb/Downloads/pathreview-ai301-fa26-s3/core/config.py:7: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.14/migration/
    class Settings(BaseSettings):

.venv/lib/python3.11/site-packages/passlib/utils/__init__.py:854
  /Users/aryahb/Downloads/pathreview-ai301-fa26-s3/.venv/lib/python3.11/site-packages/passlib/utils/__init__.py:854: DeprecationWarning: 'crypt' is deprecated and slated for removal in Python 3.13
    from crypt import crypt as _crypt

tests/unit/test_review_service.py::TestReviewService::test_list_reviews_page_2_returns_correct_offset
  /opt/homebrew/Cellar/python@3.11/3.11.15_3/Frameworks/Python.framework/Versions/3.11/lib/python3.11/unittest/mock.py:2133: RuntimeWarning: coroutine 'AsyncMockMixin._execute_mock_call' was never awaited
    setattr(_type, entry, MagicProxy(entry, self))
  Enable tracemalloc to get traceback where the object was allocated.
  See https://docs.pytest.org/en/stable/how-to/capture-warnings.html#resource-warnings for more info.

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================= 385 passed, 53 xfailed, 3 warnings in 34.35s =================

Exit status: 0
```

### test-integration

```text
$ make test-integration
.venv/bin/pytest tests/integration -v -m integration
============================= test session starts ==============================
platform darwin -- Python 3.11.15, pytest-9.1.1, pluggy-1.7.0 -- /Users/aryahb/Downloads/pathreview-ai301-fa26-s3/.venv/bin/python
cachedir: .pytest_cache
hypothesis profile 'default'
benchmark: 5.3.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /Users/aryahb/Downloads/pathreview-ai301-fa26-s3
configfile: pyproject.toml
plugins: pytest_httpserver-1.2.0, hypothesis-6.170.1, cov-7.1.0, asyncio-1.4.0, benchmark-5.3.0, platformdirs-4.13.4, anyio-4.15.1
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 6 items

tests/integration/test_rate_limit_headers.py::test_limit_is_enforced_with_real_redis PASSED [ 16%]
tests/integration/test_rate_limiter_redis.py::TestRateLimiterRedis::test_counts_remaining_and_denies_at_limit PASSED [ 33%]
tests/integration/test_rate_limiter_redis.py::TestRateLimiterRedis::test_entries_outside_window_are_pruned PASSED [ 50%]
tests/integration/test_rate_limiter_redis.py::TestRateLimiterRedis::test_key_expires_after_window_plus_one PASSED [ 66%]
tests/integration/test_rate_limiter_redis.py::TestRateLimiterRedis::test_concurrent_requests_admit_exactly_the_limit PASSED [ 83%]
tests/integration/test_rate_limiter_redis.py::TestRateLimiterRedis::test_fails_open_when_redis_is_unreachable PASSED [100%]

=============================== warnings summary ===============================
core/config.py:7
  /Users/aryahb/Downloads/pathreview-ai301-fa26-s3/core/config.py:7: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.14/migration/
    class Settings(BaseSettings):

.venv/lib/python3.11/site-packages/passlib/utils/__init__.py:854
  /Users/aryahb/Downloads/pathreview-ai301-fa26-s3/.venv/lib/python3.11/site-packages/passlib/utils/__init__.py:854: DeprecationWarning: 'crypt' is deprecated and slated for removal in Python 3.13
    from crypt import crypt as _crypt

api/main.py:100
  /Users/aryahb/Downloads/pathreview-ai301-fa26-s3/api/main.py:100: DeprecationWarning: 
          on_event is deprecated, use lifespan event handlers instead.
  
          Read more about it in the
          [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).
          
    @app.on_event("startup")

.venv/lib/python3.11/site-packages/fastapi/applications.py:4745
  /Users/aryahb/Downloads/pathreview-ai301-fa26-s3/.venv/lib/python3.11/site-packages/fastapi/applications.py:4745: DeprecationWarning: 
          on_event is deprecated, use lifespan event handlers instead.
  
          Read more about it in the
          [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).
          
    return self.router.on_event(event_type)  # ty: ignore[deprecated]

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================== 6 passed, 4 warnings in 18.52s ========================

Exit status: 0
```

### lint

```text
$ make lint
.venv/bin/ruff check .
All checks passed!

Exit status: 0
```

### typecheck

```text
$ make typecheck
.venv/bin/mypy api/ core/ ingestion/ rag/ agent/ safety/
Success: no issues found in 77 source files

Exit status: 0
```

## Captured reproduction output

```text
$ curl -sS http://127.0.0.1:8010/health
{"detail":{"status":"unhealthy","dependencies":{"postgres":"unhealthy","redis":"unhealthy","vector_db":"healthy"},"safety_events_last_hour":0,"timestamp":"2026-10-26T21:38:56.742943"}}
Exit status: 0

$ .venv/bin/python -c "import redis; from core.config import settings; print(redis.Redis.from_url(settings.redis_url).delete('rate_limit:127.0.0.1'))"
0

Exit status: 0

$ curl -sS -i http://127.0.0.1:8010/
HTTP/1.1 200 OK
date: Mon, 26 Oct 2026 21:38:56 GMT
server: uvicorn
content-length: 57
content-type: application/json
x-ratelimit-remaining: 59
x-ratelimit-limit: 60
vary: Origin
x-request-id: 097e31aa-dd61-4cab-b9cf-f6e9c60bdfa0

{"message":"PathReview API is running","version":"1.0.0"}
Exit status: 0

$ .venv/bin/python -c "import redis; from core.config import settings; print(redis.Redis.from_url(settings.redis_url).delete('rate_limit:127.0.0.1'))"
1

Exit status: 0

$ for i in $(seq 1 200); do curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8010/; done | sort | uniq -c
  60 200
 140 429

Exit status: 0

$ curl -sS -i http://127.0.0.1:8010/
HTTP/1.1 429 Too Many Requests
date: Mon, 26 Oct 2026 21:38:58 GMT
server: uvicorn
retry-after: 60
content-length: 32
content-type: application/json
x-ratelimit-remaining: 0
x-ratelimit-limit: 60
vary: Origin
x-request-id: 1d739d5f-a54d-4eac-baac-b9fe36ff9371

{"detail":"Rate limit exceeded"}
Exit status: 0

$ for i in $(seq 1 200); do curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8010/health; done | sort | uniq -c
 200 503

Exit status: 0

$ .venv/bin/python -c "import redis; from core.config import settings; print(redis.Redis.from_url(settings.redis_url).delete('rate_limit:127.0.0.1'))"
1

Exit status: 0

$ for i in $(seq 1 50); do curl -s -o /dev/null -w '%{http_code}\n' -X POST http://127.0.0.1:8010/auth/login -d "username=user1@example.com&password=wrong-password-$i"; done | sort | uniq -c
  50 401

Exit status: 0

$ curl -sS -i -X POST http://127.0.0.1:8010/auth/login -d 'username=user1@example.com&password=wrong-password-sample' 
HTTP/1.1 401 Unauthorized
date: Mon, 26 Oct 2026 21:39:12 GMT
server: uvicorn
www-authenticate: Bearer
content-length: 38
content-type: application/json
x-ratelimit-remaining: 9
x-ratelimit-limit: 60
vary: Origin
x-request-id: 6104aff0-645f-44cd-8aef-490005cce798

{"detail":"Invalid email or password"}
Exit status: 0

$ .venv/bin/python -c "import redis; from core.config import settings; print(redis.Redis.from_url(settings.redis_url).delete('rate_limit:testclient'))"
0

Exit status: 0

$ .venv/bin/python /private/tmp/unit4-evidence/trace_limiter.py
middleware stack: ['RequestIDMiddleware', 'CORSMiddleware', 'RateLimitMiddleware']
route count: 6
2026-10-26 17:39:16 [info     ] rate_limit_allowed             current_count=1 identifier=testclient limit=60 request_id=9f7452b2-4255-4dd6-b658-679b3bc3af24
2026-10-26 17:39:16 [info     ] rate_limit_allowed             current_count=2 identifier=testclient limit=60 request_id=3c1fe7e4-dbe6-4b0e-824d-a38794adad01
2026-10-26 17:39:16 [info     ] rate_limit_allowed             current_count=3 identifier=testclient limit=60 request_id=13444113-2d7e-4c35-9464-8158aa4f248d
2026-10-26 17:39:16 [info     ] rate_limit_allowed             current_count=4 identifier=testclient limit=60 request_id=b6839441-1d1a-4eba-8413-e2f627c8b585
2026-10-26 17:39:16 [info     ] rate_limit_allowed             current_count=5 identifier=testclient limit=60 request_id=f91d1071-f62a-4b86-af18-7ced0c95e63b
2026-10-26 17:39:16 [info     ] rate_limit_allowed             current_count=6 identifier=testclient limit=60 request_id=304314be-622d-4268-a97c-5db0a3da7717
2026-10-26 17:39:16 [info     ] rate_limit_allowed             current_count=7 identifier=testclient limit=60 request_id=2b5d06a0-981e-447a-8ef3-1327f0a12d01
2026-10-26 17:39:16 [info     ] rate_limit_allowed             current_count=8 identifier=testclient limit=60 request_id=49704201-490b-4d04-bb11-2b1a647c7b2b
2026-10-26 17:39:16 [info     ] rate_limit_allowed             current_count=9 identifier=testclient limit=60 request_id=70cb17fa-841e-4edd-8153-500d02686221
2026-10-26 17:39:16 [info     ] rate_limit_allowed             current_count=10 identifier=testclient limit=60 request_id=96cf499a-644c-4d4a-bc14-92e8697977a2
2026-10-26 17:39:16 [info     ] rate_limit_allowed             current_count=11 identifier=testclient limit=60 request_id=2738cab2-1b09-4fa1-b7a9-c2f3409e0bd3
2026-10-26 17:39:16 [info     ] rate_limit_allowed             current_count=12 identifier=testclient limit=60 request_id=fccf1c39-6b22-4fcf-910d-6b2ef006ef7e
2026-10-26 17:39:16 [info     ] rate_limit_allowed             current_count=13 identifier=testclient limit=60 request_id=1c4b31f6-c6ee-436e-82b4-5711e8e4b4cf
2026-10-26 17:39:16 [info     ] rate_limit_allowed             current_count=14 identifier=testclient limit=60 request_id=f3065180-a087-4ae3-a6bd-1db99afd6e82
2026-10-26 17:39:16 [info     ] rate_limit_allowed             current_count=15 identifier=testclient limit=60 request_id=19452517-68e6-465b-b01a-3794e2cdd2b1
2026-10-26 17:39:16 [info     ] rate_limit_allowed             current_count=16 identifier=testclient limit=60 request_id=7699f61c-edf9-476d-952c-30454e2e1657
2026-10-26 17:39:16 [info     ] rate_limit_allowed             current_count=17 identifier=testclient limit=60 request_id=1027f49b-590e-4838-a0c0-bf77ff7ebb9e
2026-10-26 17:39:16 [info     ] rate_limit_allowed             current_count=18 identifier=testclient limit=60 request_id=eb04c54c-7883-4822-893b-0c7b4c9237f6
2026-10-26 17:39:16 [info     ] rate_limit_allowed             current_count=19 identifier=testclient limit=60 request_id=93070171-2084-4f30-b244-c13521a0bbe2
2026-10-26 17:39:16 [info     ] rate_limit_allowed             current_count=20 identifier=testclient limit=60 request_id=a74f7ba9-41cb-4d63-9d19-52bc1039ff8c
2026-10-26 17:39:16 [error    ] postgres_health_check_failed   error="Textual SQL expression 'SELECT 1' should be explicitly declared as text('SELECT 1')" request_id=0aae05fd-debc-46d9-956b-ba046a35338e
2026-10-26 17:39:16 [error    ] redis_health_check_failed      error="'Settings' object has no attribute 'redis_host'" request_id=0aae05fd-debc-46d9-956b-ba046a35338e
2026-10-26 17:39:16 [debug    ] vector_db_health_check_passed  request_id=0aae05fd-debc-46d9-956b-ba046a35338e
2026-10-26 17:39:16 [error    ] postgres_health_check_failed   error="Textual SQL expression 'SELECT 1' should be explicitly declared as text('SELECT 1')" request_id=01967e3d-ef55-4584-95be-1644991077b0
2026-10-26 17:39:16 [error    ] redis_health_check_failed      error="'Settings' object has no attribute 'redis_host'" request_id=01967e3d-ef55-4584-95be-1644991077b0
2026-10-26 17:39:16 [debug    ] vector_db_health_check_passed  request_id=01967e3d-ef55-4584-95be-1644991077b0
2026-10-26 17:39:16 [error    ] postgres_health_check_failed   error="Textual SQL expression 'SELECT 1' should be explicitly declared as text('SELECT 1')" request_id=3f7ac410-77a9-4252-817e-b0907f4ad732
2026-10-26 17:39:16 [error    ] redis_health_check_failed      error="'Settings' object has no attribute 'redis_host'" request_id=3f7ac410-77a9-4252-817e-b0907f4ad732
2026-10-26 17:39:16 [debug    ] vector_db_health_check_passed  request_id=3f7ac410-77a9-4252-817e-b0907f4ad732
2026-10-26 17:39:16 [error    ] postgres_health_check_failed   error="Textual SQL expression 'SELECT 1' should be explicitly declared as text('SELECT 1')" request_id=aa564734-8276-40d5-985d-63bfbf4d67e1
2026-10-26 17:39:16 [error    ] redis_health_check_failed      error="'Settings' object has no attribute 'redis_host'" request_id=aa564734-8276-40d5-985d-63bfbf4d67e1
2026-10-26 17:39:16 [debug    ] vector_db_health_check_passed  request_id=aa564734-8276-40d5-985d-63bfbf4d67e1
2026-10-26 17:39:16 [error    ] postgres_health_check_failed   error="Textual SQL expression 'SELECT 1' should be explicitly declared as text('SELECT 1')" request_id=c4d39f63-b33a-4f08-ae3b-e1cac18c2368
2026-10-26 17:39:16 [error    ] redis_health_check_failed      error="'Settings' object has no attribute 'redis_host'" request_id=c4d39f63-b33a-4f08-ae3b-e1cac18c2368
2026-10-26 17:39:16 [debug    ] vector_db_health_check_passed  request_id=c4d39f63-b33a-4f08-ae3b-e1cac18c2368
2026-10-26 17:39:16 [error    ] postgres_health_check_failed   error="Textual SQL expression 'SELECT 1' should be explicitly declared as text('SELECT 1')" request_id=b1571b6a-3c44-40f9-b849-87adbf1cff97
2026-10-26 17:39:16 [error    ] redis_health_check_failed      error="'Settings' object has no attribute 'redis_host'" request_id=b1571b6a-3c44-40f9-b849-87adbf1cff97
2026-10-26 17:39:16 [debug    ] vector_db_health_check_passed  request_id=b1571b6a-3c44-40f9-b849-87adbf1cff97
2026-10-26 17:39:16 [error    ] postgres_health_check_failed   error="Textual SQL expression 'SELECT 1' should be explicitly declared as text('SELECT 1')" request_id=d9a542e9-5f08-45ab-9321-9319b39bffbd
2026-10-26 17:39:16 [error    ] redis_health_check_failed      error="'Settings' object has no attribute 'redis_host'" request_id=d9a542e9-5f08-45ab-9321-9319b39bffbd
2026-10-26 17:39:16 [debug    ] vector_db_health_check_passed  request_id=d9a542e9-5f08-45ab-9321-9319b39bffbd
2026-10-26 17:39:16 [error    ] postgres_health_check_failed   error="Textual SQL expression 'SELECT 1' should be explicitly declared as text('SELECT 1')" request_id=d3e3122e-f35d-4359-99a2-20a8438e8255
2026-10-26 17:39:16 [error    ] redis_health_check_failed      error="'Settings' object has no attribute 'redis_host'" request_id=d3e3122e-f35d-4359-99a2-20a8438e8255
2026-10-26 17:39:16 [debug    ] vector_db_health_check_passed  request_id=d3e3122e-f35d-4359-99a2-20a8438e8255
2026-10-26 17:39:16 [error    ] postgres_health_check_failed   error="Textual SQL expression 'SELECT 1' should be explicitly declared as text('SELECT 1')" request_id=760de28b-0d3e-42ab-9b8d-f915f53523d5
2026-10-26 17:39:16 [error    ] redis_health_check_failed      error="'Settings' object has no attribute 'redis_host'" request_id=760de28b-0d3e-42ab-9b8d-f915f53523d5
2026-10-26 17:39:16 [debug    ] vector_db_health_check_passed  request_id=760de28b-0d3e-42ab-9b8d-f915f53523d5
2026-10-26 17:39:16 [error    ] postgres_health_check_failed   error="Textual SQL expression 'SELECT 1' should be explicitly declared as text('SELECT 1')" request_id=6ecee390-8b51-4f49-8841-ae1725dc0ffe
2026-10-26 17:39:16 [error    ] redis_health_check_failed      error="'Settings' object has no attribute 'redis_host'" request_id=6ecee390-8b51-4f49-8841-ae1725dc0ffe
2026-10-26 17:39:16 [debug    ] vector_db_health_check_passed  request_id=6ecee390-8b51-4f49-8841-ae1725dc0ffe
2026-10-26 17:39:16 [error    ] postgres_health_check_failed   error="Textual SQL expression 'SELECT 1' should be explicitly declared as text('SELECT 1')" request_id=1642b8fe-b4ff-4861-8e60-9d195376690b
2026-10-26 17:39:16 [error    ] redis_health_check_failed      error="'Settings' object has no attribute 'redis_host'" request_id=1642b8fe-b4ff-4861-8e60-9d195376690b
2026-10-26 17:39:16 [debug    ] vector_db_health_check_passed  request_id=1642b8fe-b4ff-4861-8e60-9d195376690b
2026-10-26 17:39:16 [error    ] postgres_health_check_failed   error="Textual SQL expression 'SELECT 1' should be explicitly declared as text('SELECT 1')" request_id=b68df2cd-c4a0-4b4a-aa3d-fafd44bd5da8
2026-10-26 17:39:16 [error    ] redis_health_check_failed      error="'Settings' object has no attribute 'redis_host'" request_id=b68df2cd-c4a0-4b4a-aa3d-fafd44bd5da8
2026-10-26 17:39:16 [debug    ] vector_db_health_check_passed  request_id=b68df2cd-c4a0-4b4a-aa3d-fafd44bd5da8
2026-10-26 17:39:16 [error    ] postgres_health_check_failed   error="Textual SQL expression 'SELECT 1' should be explicitly declared as text('SELECT 1')" request_id=c8b1ec7f-b10a-4714-a66d-be56be2eb5cd
2026-10-26 17:39:16 [error    ] redis_health_check_failed      error="'Settings' object has no attribute 'redis_host'" request_id=c8b1ec7f-b10a-4714-a66d-be56be2eb5cd
2026-10-26 17:39:16 [debug    ] vector_db_health_check_passed  request_id=c8b1ec7f-b10a-4714-a66d-be56be2eb5cd
2026-10-26 17:39:16 [error    ] postgres_health_check_failed   error="Textual SQL expression 'SELECT 1' should be explicitly declared as text('SELECT 1')" request_id=96f7ba93-6fb8-4be6-add9-995d8ee4fd33
2026-10-26 17:39:16 [error    ] redis_health_check_failed      error="'Settings' object has no attribute 'redis_host'" request_id=96f7ba93-6fb8-4be6-add9-995d8ee4fd33
2026-10-26 17:39:16 [debug    ] vector_db_health_check_passed  request_id=96f7ba93-6fb8-4be6-add9-995d8ee4fd33
2026-10-26 17:39:16 [error    ] postgres_health_check_failed   error="Textual SQL expression 'SELECT 1' should be explicitly declared as text('SELECT 1')" request_id=38d47762-6b01-4a78-8ba6-e3cd5065b0a3
2026-10-26 17:39:16 [error    ] redis_health_check_failed      error="'Settings' object has no attribute 'redis_host'" request_id=38d47762-6b01-4a78-8ba6-e3cd5065b0a3
2026-10-26 17:39:16 [debug    ] vector_db_health_check_passed  request_id=38d47762-6b01-4a78-8ba6-e3cd5065b0a3
2026-10-26 17:39:16 [error    ] postgres_health_check_failed   error="Textual SQL expression 'SELECT 1' should be explicitly declared as text('SELECT 1')" request_id=b08bd220-470a-422a-93ef-551a3533cfae
2026-10-26 17:39:16 [error    ] redis_health_check_failed      error="'Settings' object has no attribute 'redis_host'" request_id=b08bd220-470a-422a-93ef-551a3533cfae
2026-10-26 17:39:16 [debug    ] vector_db_health_check_passed  request_id=b08bd220-470a-422a-93ef-551a3533cfae
2026-10-26 17:39:16 [error    ] postgres_health_check_failed   error="Textual SQL expression 'SELECT 1' should be explicitly declared as text('SELECT 1')" request_id=dce029ee-a1e2-435c-ad10-32c1efff6057
2026-10-26 17:39:16 [error    ] redis_health_check_failed      error="'Settings' object has no attribute 'redis_host'" request_id=dce029ee-a1e2-435c-ad10-32c1efff6057
2026-10-26 17:39:16 [debug    ] vector_db_health_check_passed  request_id=dce029ee-a1e2-435c-ad10-32c1efff6057
2026-10-26 17:39:16 [error    ] postgres_health_check_failed   error="Textual SQL expression 'SELECT 1' should be explicitly declared as text('SELECT 1')" request_id=ff764786-449b-48cc-937b-1e07a741a8ef
2026-10-26 17:39:16 [error    ] redis_health_check_failed      error="'Settings' object has no attribute 'redis_host'" request_id=ff764786-449b-48cc-937b-1e07a741a8ef
2026-10-26 17:39:16 [debug    ] vector_db_health_check_passed  request_id=ff764786-449b-48cc-937b-1e07a741a8ef
2026-10-26 17:39:16 [error    ] postgres_health_check_failed   error="Textual SQL expression 'SELECT 1' should be explicitly declared as text('SELECT 1')" request_id=e8d810d7-9618-44e4-9651-dad2e4056308
2026-10-26 17:39:16 [error    ] redis_health_check_failed      error="'Settings' object has no attribute 'redis_host'" request_id=e8d810d7-9618-44e4-9651-dad2e4056308
2026-10-26 17:39:16 [debug    ] vector_db_health_check_passed  request_id=e8d810d7-9618-44e4-9651-dad2e4056308
2026-10-26 17:39:16 [error    ] postgres_health_check_failed   error="Textual SQL expression 'SELECT 1' should be explicitly declared as text('SELECT 1')" request_id=f1ceebaf-a1d7-47af-972a-deab255e725f
2026-10-26 17:39:16 [error    ] redis_health_check_failed      error="'Settings' object has no attribute 'redis_host'" request_id=f1ceebaf-a1d7-47af-972a-deab255e725f
2026-10-26 17:39:16 [debug    ] vector_db_health_check_passed  request_id=f1ceebaf-a1d7-47af-972a-deab255e725f
statuses: {'/': {200: 20}, '/health': {503: 20}}
2026-10-26 17:39:16 [info     ] rate_limit_allowed             current_count=21 identifier=testclient limit=60 request_id=03f28179-8f04-4a55-a89f-5c05664ebd6c
sample headers GET /: {'x-ratelimit-remaining': '39', 'x-ratelimit-limit': '60', 'x-request-id': '03f28179-8f04-4a55-a89f-5c05664ebd6c'}
check_rate_limit calls observed: 21

Exit status: 0

$ rg -n 'check_rate_limit|RateLimiter' api safety tests --glob '*.py'
api/main.py:13:from safety.rate_limiter import RateLimiter
api/main.py:48:rate_limiter = RateLimiter(redis_client)
tests/integration/test_rate_limiter_redis.py:1:"""RateLimiter against a real Redis: the Lua script's counts, pruning, TTL, and concurrency."""
tests/integration/test_rate_limiter_redis.py:11:from safety.rate_limiter import RateLimiter
tests/integration/test_rate_limiter_redis.py:29:class TestRateLimiterRedis:
tests/integration/test_rate_limiter_redis.py:30:    """Behavior of RateLimiter.check_rate_limit against a real Redis."""
tests/integration/test_rate_limiter_redis.py:34:        limiter = RateLimiter(store)
tests/integration/test_rate_limiter_redis.py:36:        results = [limiter.check_rate_limit(identifier, limit=3) for _ in range(4)]
tests/integration/test_rate_limiter_redis.py:42:        limiter = RateLimiter(store)
tests/integration/test_rate_limiter_redis.py:44:        assert limiter.check_rate_limit(identifier, limit=2, window_seconds=1) == (True, 1)
tests/integration/test_rate_limiter_redis.py:45:        assert limiter.check_rate_limit(identifier, limit=2, window_seconds=1) == (True, 0)
tests/integration/test_rate_limiter_redis.py:46:        assert limiter.check_rate_limit(identifier, limit=2, window_seconds=1) == (False, 0)
tests/integration/test_rate_limiter_redis.py:50:        assert limiter.check_rate_limit(identifier, limit=2, window_seconds=1) == (True, 1)
tests/integration/test_rate_limiter_redis.py:54:        limiter = RateLimiter(store)
tests/integration/test_rate_limiter_redis.py:56:        limiter.check_rate_limit(identifier, limit=10, window_seconds=60)
tests/integration/test_rate_limiter_redis.py:67:        limiter = RateLimiter(store)
tests/integration/test_rate_limiter_redis.py:72:                pool.map(lambda _: limiter.check_rate_limit(identifier, limit), range(20))
tests/integration/test_rate_limiter_redis.py:83:        limiter = RateLimiter(unreachable)
tests/integration/test_rate_limiter_redis.py:85:        assert limiter.check_rate_limit("unreachable-test", limit=10) == (True, 10)
safety/rate_limiter.py:30:class RateLimiter:
safety/rate_limiter.py:42:    def check_rate_limit(
api/middleware/rate_limit.py:13:from safety.rate_limiter import RateLimiter
api/middleware/rate_limit.py:32:        limiter: RateLimiter,
api/middleware/rate_limit.py:69:            self.limiter.check_rate_limit, identifier, self.limit, self.window_seconds
tests/unit/test_rate_limit_middleware.py:20:    def check_rate_limit(
tests/unit/test_rate_limiter.py:7:from safety.rate_limiter import RateLimiter
tests/unit/test_rate_limiter.py:33:class TestRateLimiter:
tests/unit/test_rate_limiter.py:34:    """Test suite for RateLimiter."""
tests/unit/test_rate_limiter.py:45:        """Create a RateLimiter instance with mocked Redis."""
tests/unit/test_rate_limiter.py:46:        return RateLimiter(mock_redis)
tests/unit/test_rate_limiter.py:55:        allowed, remaining = limiter.check_rate_limit("user123", limit=10)
tests/unit/test_rate_limiter.py:71:            allowed, remaining = limiter.check_rate_limit("user123", limit=limit)
tests/unit/test_rate_limiter.py:82:        allowed, remaining = limiter.check_rate_limit("user123", limit=limit)
tests/unit/test_rate_limiter.py:97:        allowed, remaining = limiter.check_rate_limit("user123", limit=limit)
tests/unit/test_rate_limiter.py:109:            limiter.check_rate_limit("user123", limit=10, window_seconds=60)
tests/unit/test_rate_limiter.py:127:        limiter.check_rate_limit("user1", limit=10)
tests/unit/test_rate_limiter.py:128:        limiter.check_rate_limit("user2", limit=10)
tests/unit/test_rate_limiter.py:141:        limiter.check_rate_limit("test_user", limit=10)
tests/unit/test_rate_limiter.py:155:            limiter.check_rate_limit("user123", limit=10)
tests/unit/test_rate_limiter.py:174:        limiter.check_rate_limit("user123", limit=10, window_seconds=window)
tests/unit/test_rate_limiter.py:190:            limiter.check_rate_limit("user123", limit=10, window_seconds=custom_window)
tests/unit/test_rate_limiter.py:203:            allowed, remaining = limiter.check_rate_limit("user123", limit=10)
tests/unit/test_rate_limiter.py:213:        allowed, remaining = limiter.check_rate_limit("user123", limit=0)
tests/unit/test_rate_limiter.py:223:        allowed, remaining = limiter.check_rate_limit("user123", limit=-1)
tests/unit/test_rate_limiter.py:236:        allowed, remaining = limiter.check_rate_limit("user123", limit=large_limit)
tests/unit/test_rate_limiter.py:248:        result = limiter.check_rate_limit("user123", limit=10)
tests/unit/test_rate_limiter.py:264:        allowed1, remaining1 = limiter.check_rate_limit("user123", limit=10)
tests/unit/test_rate_limiter.py:270:        allowed2, remaining2 = limiter.check_rate_limit("user123", limit=10)
tests/unit/test_rate_limiter.py:283:            limiter.check_rate_limit("user123", limit=10, window_seconds=60)
tests/unit/test_rate_limiter.py:288:            limiter.check_rate_limit("user123", limit=10, window_seconds=60)
tests/unit/test_rate_limiter.py:301:        limiter.check_rate_limit("192.168.1.1", limit=100)
tests/unit/test_rate_limiter.py:315:        limiter.check_rate_limit(api_key, limit=1000)
tests/unit/test_rate_limiter.py:329:            limiter.check_rate_limit("user123", limit=10)
tests/unit/test_rate_limiter.py:330:            limiter.check_rate_limit("user123", limit=10)

Exit status: 0

$ rg -n -i 'X-RateLimit|429|too_many' api safety tests --glob '*.py'
tests/integration/test_rate_limit_headers.py:16:    """The first `limit` requests pass with decreasing remaining counts; the next one gets 429."""
tests/integration/test_rate_limit_headers.py:26:            assert response.headers["X-RateLimit-Limit"] == str(limit)
tests/integration/test_rate_limit_headers.py:27:            assert response.headers["X-RateLimit-Remaining"] == str(limit - i)
tests/integration/test_rate_limit_headers.py:30:        assert denied.status_code == 429
tests/integration/test_rate_limit_headers.py:32:        assert denied.headers["X-RateLimit-Remaining"] == "0"
api/middleware/rate_limit.py:24:    through unchanged. Allowed responses carry X-RateLimit-Limit and
api/middleware/rate_limit.py:25:    X-RateLimit-Remaining. Denied requests get HTTP 429 with a Retry-After
api/middleware/rate_limit.py:62:            The downstream response with rate-limit headers, or a 429 response.
api/middleware/rate_limit.py:76:                status_code=429,
api/middleware/rate_limit.py:79:            response.headers["X-RateLimit-Remaining"] = "0"
api/middleware/rate_limit.py:82:            response.headers["X-RateLimit-Remaining"] = str(remaining)
api/middleware/rate_limit.py:84:        response.headers["X-RateLimit-Limit"] = str(self.limit)
api/main.py:50:# Added before CORS so it runs innermost: a 429 still passes through the CORS and request-ID
tests/unit/test_rate_limit_middleware.py:45:    """Headers, 429 handling, exemptions, and identifier for RateLimitMiddleware."""
tests/unit/test_rate_limit_middleware.py:54:        assert response.headers["X-RateLimit-Limit"] == "60"
tests/unit/test_rate_limit_middleware.py:55:        assert response.headers["X-RateLimit-Remaining"] == "59"
tests/unit/test_rate_limit_middleware.py:57:    def test_denied_request_returns_429_with_retry_after(self) -> None:
tests/unit/test_rate_limit_middleware.py:63:        assert response.status_code == 429
tests/unit/test_rate_limit_middleware.py:66:        assert response.headers["X-RateLimit-Limit"] == "60"
tests/unit/test_rate_limit_middleware.py:67:        assert response.headers["X-RateLimit-Remaining"] == "0"
tests/unit/test_rate_limit_middleware.py:77:        assert "X-RateLimit-Limit" not in response.headers
tests/unit/test_rate_limit_middleware.py:86:        assert "X-RateLimit-Limit" not in response.headers
tests/unit/test_rate_limit_middleware.py:103:        assert response.headers["X-RateLimit-Remaining"] == str(remaining)
tests/unit/test_rate_limit_middleware.py:113:        assert response.headers["X-RateLimit-Remaining"] == "60"

Exit status: 0

$ rg -n 'check_rate_limit' api safety --glob '*.py'
safety/rate_limiter.py:42:    def check_rate_limit(
api/middleware/rate_limit.py:69:            self.limiter.check_rate_limit, identifier, self.limit, self.window_seconds

Exit status: 0
```

## Upstream CI correction after PR #268

First CI run `40406823549`: frontend, lint, typecheck, and unit jobs passed; integration collection failed with `ModuleNotFoundError: No module named 'psycopg'` while importing the real app. Reproduced locally using the workflow's original `DATABASE_URL=postgresql://pathreview:pathreview@localhost:5432/pathreview_test`. The app uses an async engine and already declares asyncpg. Changed only that workflow URL to `postgresql+asyncpg://...` in commit `cc74654`; the runtime implementation is unchanged.

Focused after-check, using CI's database URL, REDIS_URL and LLM_PROVIDER:

```bash
DATABASE_URL=postgresql+asyncpg://pathreview:pathreview@localhost:5432/pathreview_test REDIS_URL=redis://localhost:6379/0 LLM_PROVIDER=mock .venv/bin/pytest tests/integration -v --tb=short
```

Actual result: **6 passed, 4 warnings in 6.49s**, exit 0. No runtime source changed, so the previously passing unit/lint/typecheck/frontend checks were not repeated locally. The final head is recorded with its exact verified SHA in the Unit 4 write-up. Raw failing and passing collection/run outputs are preserved under Unit 4 `evidence/ci-db-url-before.txt` and `evidence/ci-db-url-after.txt`.

Final upstream verification: CI run `40407240487` completed successfully on `cc74654eeb2575ee35d19fdf2f2cbe584525bf0d`, with all five jobs passing. See Unit 4 `ci-status.md` and the raw `evidence/ci-final-status.json`.
