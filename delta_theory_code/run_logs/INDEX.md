# Index of recorded runs

Every Python run made while developing the theory, with its exact command and the output it printed, in time order.
`simulations/` holds the runs that produced or checked results; `document_tooling/` holds runs that built or checked the LaTeX documents.
Commands refer to `/home/claude/<dir>`, which is `scripts/<dir>` in this package. Early runs sometimes used inline code (`python3 - << EOF`), which is preserved in the log.
Some scripts were revised after a run; the log shows what was actually run at the time, and `scripts/` holds the final versions.

## Simulations and checks

| # | Time (UTC) | Purpose | File |
|---|---|---|---|
| 001 | 2026-09-23 07:30 | Simulate two contact-coupled clocks | simulations/001_2026-09-23T0730_simulate_two_contact_coupled_clocks.txt |
| 002 | 2026-09-23 07:33 | Simulate three contact-coupled clocks | simulations/002_2026-09-23T0733_simulate_three_contact_coupled_clocks.txt |
| 003 | 2026-09-23 07:56 | Resonant pair, circle map staircase, turnover test | simulations/003_2026-09-23T0756_resonant_pair_circle_map_staircase_turnover_test.txt |
| 004 | 2026-09-23 08:50 | Test the working note's interaction equation (14): residual and collective frequency | simulations/004_2026-09-23T0850_test_the_working_note_s_interaction_equation_14_residual_and.txt |
| 005 | 2026-09-23 08:51 | Check different-kappa without delay, and mutual full uptake | simulations/005_2026-09-23T0851_check_different_kappa_without_delay_and_mutual_full_uptake.txt |
| 006 | 2026-09-23 09:08 | Two-part universe: elastic exchange vs one-step latency | simulations/006_2026-09-23T0908_two_part_universe_elastic_exchange_vs_one_step_latency.txt |
| 007 | 2026-09-23 09:09 | Many-part universe: elastic exchange vs one-round latency | simulations/007_2026-09-23T0909_many_part_universe_elastic_exchange_vs_one_round_latency.txt |
| 008 | 2026-09-23 09:10 | Test whether elastic exchange thermalizes: equipartition across masses | simulations/008_2026-09-23T0910_test_whether_elastic_exchange_thermalizes_equipartition_acro.txt |
| 009 | 2026-09-23 09:20 | Test parameter-free birth/death rules against the philosophy's criteria | simulations/009_2026-09-23T0920_test_parameter_free_birth_death_rules_against_the_philosophy.txt |
| 010 | 2026-09-23 09:21 | Run rule R1 longer to see whether births and deaths balance | simulations/010_2026-09-23T0921_run_rule_r1_longer_to_see_whether_births_and_deaths_balance.txt |
| 011 | 2026-09-23 09:22 | Probe intermediate merge/bounce balance between collapse and fragmentation | simulations/011_2026-09-23T0922_probe_intermediate_merge_bounce_balance_between_collapse_and.txt |
| 012 | 2026-09-23 09:28 | Simulate clusters that keep their members, with Ch. 14's reconciliation burden | simulations/012_2026-09-23T0928_simulate_clusters_that_keep_their_members_with_ch_14_s_recon.txt |
| 013 | 2026-09-23 09:29 | Test whether crossover births regulate the remainder toward a set point | simulations/013_2026-09-23T0929_test_whether_crossover_births_regulate_the_remainder_toward_.txt |
| 014 | 2026-09-23 09:29 | Run the thermostat test longer to see where the remainder settles | simulations/014_2026-09-23T0929_run_the_thermostat_test_longer_to_see_where_the_remainder_se.txt |
| 015 | 2026-09-23 09:32 | Local meetings on the relational network: do births and deaths balance? | simulations/015_2026-09-23T0932_local_meetings_on_the_relational_network_do_births_and_death.txt |
| 016 | 2026-09-23 09:33 | Does the thermostat survive locality? Births and bounces on the relational network | simulations/016_2026-09-23T0933_does_the_thermostat_survive_locality_births_and_bounces_on_t.txt |
| 020 | 2026-09-23 12:45 | Scan the absorption probability q to locate the edge between growth and collapse | simulations/020_2026-09-23T1245_scan_the_absorption_probability_q_to_locate_the_edge_between.txt |
| 021 | 2026-09-23 12:46 | Fine scan near the transition with two seeds, tracking the largest part | simulations/021_2026-09-23T1246_fine_scan_near_the_transition_with_two_seeds_tracking_the_la.txt |
| 022 | 2026-09-23 12:48 | Measure the mass spectrum and lifetimes near the edge and away from it | simulations/022_2026-09-23T1248_measure_the_mass_spectrum_and_lifetimes_near_the_edge_and_aw.txt |
| 023 | 2026-09-23 12:49 | Check whether the tails are straight power laws or curved | simulations/023_2026-09-23T1249_check_whether_the_tails_are_straight_power_laws_or_curved.txt |
| 024 | 2026-09-23 12:59 | Check what exchange on stale records does to each part and to the pair's totals | simulations/024_2026-09-23T1259_check_what_exchange_on_stale_records_does_to_each_part_and_t.txt |
| 025 | 2026-09-23 12:59 | Records plus leakage, in the collapse phase (q = 0.9) | simulations/025_2026-09-23T1259_records_plus_leakage_in_the_collapse_phase_q_0_9.txt |
| 026 | 2026-09-23 13:00 | Local network with records and leakage versus without, at q = 0.6 | simulations/026_2026-09-23T1300_local_network_with_records_and_leakage_versus_without_at_q_0.txt |
| 027 | 2026-09-23 13:06 | Baseline on the local network: where does collapse begin? | simulations/027_2026-09-23T1306_baseline_on_the_local_network_where_does_collapse_begin.txt |
| 028 | 2026-09-23 13:06 | Option (a): primordial light at 10% and 30% of the whole | simulations/028_2026-09-23T1306_option_a_primordial_light_at_10_and_30_of_the_whole.txt |
| 029 | 2026-09-23 13:07 | Option (b): residues live on the relation itself | simulations/029_2026-09-23T1307_option_b_residues_live_on_the_relation_itself.txt |
| 030 | 2026-09-23 13:07 | Test a perspectival event rule: the initiator decides from its own row of the matrix | simulations/030_2026-09-23T1307_test_a_perspectival_event_rule_the_initiator_decides_from_it.txt |
| 031 | 2026-09-23 13:13 | Build the two-view rule on the relational network and test whether its growth is self-similar | simulations/031_2026-09-23T1313_build_the_two_view_rule_on_the_relational_network_and_test_w.txt |
| 032 | 2026-09-23 13:21 | Measure the geometry of the relational network the two-view universe grows | simulations/032_2026-09-23T1321_measure_the_geometry_of_the_relational_network_the_two_view_.txt |
| 033 | 2026-09-23 13:29 | Verify the identity linking the Minkowski interval of two parts to their pair matrix | simulations/033_2026-09-23T1329_verify_the_identity_linking_the_minkowski_interval_of_two_pa.txt |
| 034 | 2026-09-23 13:29 | Test the causal rule: two views for spacelike pairs, one-way for timelike pairs | simulations/034_2026-09-23T1329_test_the_causal_rule_two_views_for_spacelike_pairs_one_way_f.txt |
| 035 | 2026-09-23 13:30 | Test whether making activity independent of size (no speed-up for giants) changes the outcome | simulations/035_2026-09-23T1330_test_whether_making_activity_independent_of_size_no_speed_up.txt |
| 036 | 2026-09-23 13:33 | Recheck equipartition under the size-independent activity rule | simulations/036_2026-09-23T1333_recheck_equipartition_under_the_size_independent_activity_ru.txt |
| 037 | 2026-09-23 13:33 | Add relational death: a part contained by every neighbour is taken in by its strongest registrant | simulations/037_2026-09-23T1333_add_relational_death_a_part_contained_by_every_neighbour_is_.txt |
| 038 | 2026-09-23 13:34 | Relational death shared among all neighbours instead of given to the strongest one | simulations/038_2026-09-23T1334_relational_death_shared_among_all_neighbours_instead_of_give.txt |
| 039 | 2026-09-23 13:34 | Is the dust between the giants structured locally, or degenerate? | simulations/039_2026-09-23T1334_is_the_dust_between_the_giants_structured_locally_or_degener.txt |
| 040 | 2026-09-23 13:38 | Check equipartition under the derived rule (pairs meet at a rate proportional to cosh of relative rapidity) | simulations/040_2026-09-23T1338_check_equipartition_under_the_derived_rule_pairs_meet_at_a_r.txt |
| 041 | 2026-09-23 13:39 | Run the universe with the derived activity rule: each relation hosts encounters at rate cosh(relative rapidity) | simulations/041_2026-09-23T1339_run_the_universe_with_the_derived_activity_rule_each_relatio.txt |
| 042 | 2026-09-23 13:40 | One process, one clock: each part ticks equally and meets a neighbour weighted by cosh of relative rapidity | simulations/042_2026-09-23T1340_one_process_one_clock_each_part_ticks_equally_and_meets_a_ne.txt |
| 043 | 2026-09-23 13:41 | Derived rule: equal clocks, registration arriving only as propagating difference (Doppler factor along one direction) | simulations/043_2026-09-23T1341_derived_rule_equal_clocks_registration_arriving_only_as_prop.txt |
| 044 | 2026-09-23 13:41 | Equipartition check under the derived activity rule | simulations/044_2026-09-23T1341_equipartition_check_under_the_derived_activity_rule.txt |
| 045 | 2026-09-23 13:47 | Verify the reduction: selves minus relations compares the mass angle with the motion angle | simulations/045_2026-09-23T1347_verify_the_reduction_selves_minus_relations_compares_the_mas.txt |
| 046 | 2026-09-23 13:48 | Run the channel test: log every encounter's channel and trace how far each one's influence spreads | simulations/046_2026-09-23T1348_run_the_channel_test_log_every_encounter_s_channel_and_trace.txt |
| 047 | 2026-09-23 13:48 | Compare the channels: frequency, geometry, mass-motion conversion, and reach through the network | simulations/047_2026-09-23T1348_compare_the_channels_frequency_geometry_mass_motion_conversi.txt |
| 048 | 2026-09-23 13:49 | Trace influence over a much longer window so reach can actually develop | simulations/048_2026-09-23T1349_trace_influence_over_a_much_longer_window_so_reach_can_actua.txt |
| 049 | 2026-09-23 13:52 | Grow universes from the first asymmetry (two parts) and measure the geometry of their relational network | simulations/049_2026-09-23T1352_grow_universes_from_the_first_asymmetry_two_parts_and_measur.txt |
| 050 | 2026-09-23 13:53 | Estimate the spectral dimension and ball growth of the surviving universe's network | simulations/050_2026-09-23T1353_estimate_the_spectral_dimension_and_ball_growth_of_the_survi.txt |
| 051 | 2026-09-23 13:53 | Survival of the first asymmetry, and whether giants act as shortcuts in the network | simulations/051_2026-09-23T1353_survival_of_the_first_asymmetry_and_whether_giants_act_as_sh.txt |
| 052 | 2026-09-23 13:59 | Measure distance by how different connected parts are, and the dimension a processor would see at each reach | simulations/052_2026-09-23T1359_measure_distance_by_how_different_connected_parts_are_and_th.txt |
| 053 | 2026-09-23 14:03 | Relay what parts know about each other through their encounters, and measure how stale knowledge becomes with distance | simulations/053_2026-09-23T1403_relay_what_parts_know_about_each_other_through_their_encount.txt |
| 054 | 2026-09-23 14:05 | Find universes that survive their first asymmetry, for a robustness check | simulations/054_2026-09-23T1405_find_universes_that_survive_their_first_asymmetry_for_a_robu.txt |
| 055 | 2026-09-23 14:06 | Horizon and dimension at the horizon for four universes, smaller size | simulations/055_2026-09-23T1406_horizon_and_dimension_at_the_horizon_for_four_universes_smal.txt |
| 056 | 2026-09-23 14:08 | Robust horizon measurement: replace sources that die, sample repeatedly, four universes at the smaller size | simulations/056_2026-09-23T1408_robust_horizon_measurement_replace_sources_that_die_sample_r.txt |
| 057 | 2026-09-23 14:09 | Repeat at a larger size to see whether the horizon and its dimension drift as the universe grows | simulations/057_2026-09-23T1409_repeat_at_a_larger_size_to_see_whether_the_horizon_and_its_d.txt |
| 058 | 2026-09-23 14:12 | Records in the derived dynamics: relations carry the mismatch between what parts claim and what they give; test for binding | simulations/058_2026-09-23T1412_records_in_the_derived_dynamics_relations_carry_the_mismatch.txt |
| 059 | 2026-09-23 14:13 | Find universes that survive their first asymmetry when parts act on records | simulations/059_2026-09-23T1413_find_universes_that_survive_their_first_asymmetry_when_parts.txt |
| 060 | 2026-09-23 14:13 | Measure binding in three universes where parts act on records | simulations/060_2026-09-23T1413_measure_binding_in_three_universes_where_parts_act_on_record.txt |
| 061 | 2026-09-23 14:15 | Test whether binding behaves like a force: bound structures, bond lifetimes, and dependence on relational distance | simulations/061_2026-09-23T1415_test_whether_binding_behaves_like_a_force_bound_structures_b.txt |
| 062 | 2026-09-23 14:17 | Derive the binding condition: debt times continuity against the kinetic surplus of relative motion | simulations/062_2026-09-23T1417_derive_the_binding_condition_debt_times_continuity_against_t.txt |
| 063 | 2026-09-23 14:17 | Track every bond through its members' encounters: which encounters break it, which it survives | simulations/063_2026-09-23T1417_track_every_bond_through_its_members_encounters_which_encoun.txt |
| 064 | 2026-09-23 14:19 | Test whether bonds in relative motion build long-lived structures, and whether structures outlast their members | simulations/064_2026-09-23T1419_test_whether_bonds_in_relative_motion_build_long_lived_struc.txt |
| 067 | 2026-09-23 14:28 | Derive and check: latency turns the exchange's reflection into a rotation with unit-modulus phases | simulations/067_2026-09-23T1428_derive_and_check_latency_turns_the_exchange_s_reflection_int.txt |
| 068 | 2026-09-23 14:32 | Try A2 with actual exchanges: a source pair, two relay paths of different length, one receiver | simulations/068_2026-09-23T1432_try_a2_with_actual_exchanges_a_source_pair_two_relay_paths_o.txt |
| 069 | 2026-09-23 14:32 | Re-run with the source pair exchanging last in each tick, so its oscillation can leak into the relay paths | simulations/069_2026-09-23T1432_re_run_with_the_source_pair_exchanging_last_in_each_tick_so_.txt |
| 070 | 2026-09-23 14:33 | Enforce one encounter per part per tick and use records as the latency; test transmission and interference | simulations/070_2026-09-23T1433_enforce_one_encounter_per_part_per_tick_and_use_records_as_t.txt |
| 071 | 2026-09-23 14:33 | Lock-in test of superposition: does the two-path response equal the sum of the one-path responses, and does their phase track path length? | simulations/071_2026-09-23T1433_lock_in_test_of_superposition_does_the_two_path_response_equ.txt |
| 072 | 2026-09-23 14:34 | Is the linearized evolution of a whole network lossless (all modes on the unit circle), not just an isolated pair? | simulations/072_2026-09-23T1434_is_the_linearized_evolution_of_a_whole_network_lossless_all_.txt |
| 073 | 2026-09-23 14:35 | Check that the lossless evolution holds on a random network, around non-uniform states, over long times | simulations/073_2026-09-23T1435_check_that_the_lossless_evolution_holds_on_a_random_network_.txt |
| 074 | 2026-09-23 14:35 | How far from uniformity does the lossless regime extend? | simulations/074_2026-09-23T1435_how_far_from_uniformity_does_the_lossless_regime_extend.txt |
| 075 | 2026-09-23 14:38 | Replace the shared flux (a view from nowhere) with each part's own correction, and test finite unevenness | simulations/075_2026-09-23T1438_replace_the_shared_flux_a_view_from_nowhere_with_each_part_s.txt |
| 076 | 2026-09-23 14:39 | Test a third form: the relation remembers the pair's split and executes the registered swap on current totals | simulations/076_2026-09-23T1439_test_a_third_form_the_relation_remembers_the_pair_s_split_an.txt |
| 077 | 2026-09-23 21:35 | A3 test: do registration rates follow squared amplitudes of the rotating layer? | simulations/077_2026-09-23T2135_a3_test_do_registration_rates_follow_squared_amplitudes_of_t.txt |
| 078 | 2026-09-23 21:37 | Search for the conserved quadratic quantity of the rotating layer (the candidate for total probability) | simulations/078_2026-09-23T2137_search_for_the_conserved_quadratic_quantity_of_the_rotating_.txt |
| 079 | 2026-09-23 21:39 | Search for a conserved sum of local squares over parts and relations' memory | simulations/079_2026-09-23T2139_search_for_a_conserved_sum_of_local_squares_over_parts_and_r.txt |
| 080 | 2026-09-23 21:40 | Show the weights of the conserved local form | simulations/080_2026-09-23T2140_show_the_weights_of_the_conserved_local_form.txt |
| 081 | 2026-09-23 21:45 | Inject one halving's worth of difference into a nearly even structure and follow how it spreads | simulations/081_2026-09-23T2145_inject_one_halving_s_worth_of_difference_into_a_nearly_even_.txt |
| 082 | 2026-09-23 21:45 | Single outcomes: when and where does the spread quantum reconcentrate into a full halving, versus its squared-amplitude map? | simulations/082_2026-09-23T2145_single_outcomes_when_and_where_does_the_spread_quantum_recon.txt |
| 083 | 2026-09-23 21:52 | Close Stage A: with whole-unit registration, do single outcomes follow the conserved total's density? | simulations/083_2026-09-23T2152_close_stage_a_with_whole_unit_registration_do_single_outcome.txt |
| 084 | 2026-09-23 21:53 | Rerun the Stage A closing test with errors visible | simulations/084_2026-09-23T2153_rerun_the_stage_a_closing_test_with_errors_visible.txt |
| 085 | 2026-09-23 21:53 | Strip the slow demo block from the helper module and rerun the Stage A test | simulations/085_2026-09-23T2153_strip_the_slow_demo_block_from_the_helper_module_and_rerun_t.txt |
| 086 | 2026-09-23 21:53 | Separate the rotating quantum from the lasting change it leaves, then compare single outcomes with squared amplitudes | simulations/086_2026-09-23T2153_separate_the_rotating_quantum_from_the_lasting_change_it_lea.txt |
| 087 | 2026-09-23 21:55 | B1: is there a circle symmetry acting on each part's continuity-difference plane? Globally, and locally? | simulations/087_2026-09-23T2155_b1_is_there_a_circle_symmetry_acting_on_each_part_s_continui.txt |
| 088 | 2026-09-23 21:56 | Is the dynamics unchanged when a single part changes its own frame (a true local symmetry)? | simulations/088_2026-09-23T2156_is_the_dynamics_unchanged_when_a_single_part_changes_its_own.txt |
| 089 | 2026-09-23 22:07 | Rewrite the exchange in frame-carrying form; test local relabelling symmetry and equivalence with the old rule | simulations/089_2026-09-23T2207_rewrite_the_exchange_in_frame_carrying_form_test_local_relab.txt |
| 090 | 2026-09-23 22:08 | Flat versus flux link configurations: is flux conserved, and is the flux sector stable? | simulations/090_2026-09-23T2208_flat_versus_flux_link_configurations_is_flux_conserved_and_i.txt |
| 091 | 2026-09-23 22:09 | Test 2: search every linear transformation local to one part for a symmetry of the lossless layer | simulations/091_2026-09-23T2209_test_2_search_every_linear_transformation_local_to_one_part_.txt |
| 092 | 2026-09-23 22:09 | Inspect the rare one-part transformation that commutes: is it a rotation or something trivial? | simulations/092_2026-09-23T2209_inspect_the_rare_one_part_transformation_that_commutes_is_it.txt |
| 093 | 2026-09-23 22:10 | Check for time-dependent local symmetries (a local transformation whose form rotates with time but stays local) | simulations/093_2026-09-23T2210_check_for_time_dependent_local_symmetries_a_local_transforma.txt |
| 094 | 2026-09-23 22:11 | Identify the one local transformation: a part's size direction and a conserved local size total | simulations/094_2026-09-23T2211_identify_the_one_local_transformation_a_part_s_size_directio.txt |
| 095 | 2026-09-23 22:18 | Composites alone: verify the reduced rapidity layer and find each composite's internal circles | simulations/095_2026-09-23T2218_composites_alone_verify_the_reduced_rapidity_layer_and_find_.txt |
| 096 | 2026-09-23 22:18 | Fix the import path and rerun | simulations/096_2026-09-23T2218_fix_the_import_path_and_rerun.txt |
| 097 | 2026-09-23 22:18 | Two identical composites joined by one relation: does the exchange depend only on phase differences? | simulations/097_2026-09-23T2218_two_identical_composites_joined_by_one_relation_does_the_exc.txt |
| 098 | 2026-09-23 22:19 | Repeat with the exactly conserved total and composites whose internal waves are spread out | simulations/098_2026-09-23T2219_repeat_with_the_exactly_conserved_total_and_composites_whose.txt |
| 099 | 2026-09-23 22:20 | Fix the band-energy measure, use internal waves near a quarter-turn, and extend to larger composites | simulations/099_2026-09-23T2220_fix_the_band_energy_measure_use_internal_waves_near_a_quarte.txt |
| 100 | 2026-09-23 22:22 | State-level test: does turning every internal wave of both composites by the same angle commute with their interaction? | simulations/100_2026-09-23T2222_state_level_test_does_turning_every_internal_wave_of_both_co.txt |
| 101 | 2026-09-23 22:26 | Can the joining relation compensate a local turn? And do two circulation senses survive an interaction? | simulations/101_2026-09-23T2226_can_the_joining_relation_compensate_a_local_turn_and_do_two_.txt |
| 102 | 2026-09-23 22:26 | Check whether the local rotations only turn internal waves that the other composite cannot see | simulations/102_2026-09-23T2226_check_whether_the_local_rotations_only_turn_internal_waves_t.txt |
| 103 | 2026-09-23 22:29 | Confirm that the local transformations only produce waves the other composite can never detect | simulations/103_2026-09-23T2229_confirm_that_the_local_transformations_only_produce_waves_th.txt |
| 110 | 2026-09-24 02:38 | Test the note on the Part II universe: do clocks stop, and do they synchronise (remainder of motion to zero)? | simulations/110_2026-09-24T0238_test_the_note_on_the_part_ii_universe_do_clocks_stop_and_do_.txt |
| 111 | 2026-09-24 02:41 | More universes: does the desynchronisation (motion remainder) fall as the universe ages? | simulations/111_2026-09-24T0241_more_universes_does_the_desynchronisation_motion_remainder_f.txt |
| 120 | 2026-09-24 03:04 | Test vanishing as an act: continuity stays, difference spreads to all neighbours, disturbing the field | simulations/120_2026-09-24T0304_test_vanishing_as_an_act_continuity_stays_difference_spreads.txt |
| 121 | 2026-09-24 03:06 | Check whether the new vanishing rule changes the network's space: dimension by reach and the giants' role | simulations/121_2026-09-24T0306_check_whether_the_new_vanishing_rule_changes_the_network_s_s.txt |
| 129 | 2026-09-25 03:20 | Find universes that survive their first asymmetry, for each rule (magnet/scan.py) | simulations/129_2026-09-25T0320_find_universes_that_survive_their_first_asymmetry_for_each_r.txt |
| 130 | 2026-09-25 03:28 | Polarity (magnetism) test, final version with rapidity relative to the parts own totals (magnet/polarity.py) | simulations/130_2026-09-25T0328_polarity_magnetism_test_final_version_with_rapidity_relative.txt |

## Document tooling

| # | Time (UTC) | Purpose | File |
| 104 | 2026-09-23 22:37 | Inspect the transcript format carefully (small output) | document_tooling/104_2026-09-23T2237_inspect_the_transcript_format_carefully_small_output.txt |
| 105 | 2026-09-23 22:37 | Extract assistant text around the start of Stage A | document_tooling/105_2026-09-23T2237_extract_assistant_text_around_the_start_of_stage_a.txt |
| 106 | 2026-09-23 22:37 | Print the full Stage A replies from the transcript | document_tooling/106_2026-09-23T2237_print_the_full_stage_a_replies_from_the_transcript.txt |
|---|---|---|---|
| 017 | 2026-09-23 10:33 | Fix the wide tables, recompile and render pages for inspection | document_tooling/017_2026-09-23T1033_fix_the_wide_tables_recompile_and_render_pages_for_inspectio.txt |
| 018 | 2026-09-23 10:34 | Make the numerical tags visible in box titles, keep plain-words boxes whole, recompile | document_tooling/018_2026-09-23T1034_make_the_numerical_tags_visible_in_box_titles_keep_plain_wor.txt |
| 019 | 2026-09-23 10:34 | Move the figure legend, do the final compile and copy both files to outputs | document_tooling/019_2026-09-23T1034_move_the_figure_legend_do_the_final_compile_and_copy_both_fi.txt |
| 065 | 2026-09-23 14:25 | Write the new closing chapter, splice everything into the document, and compile | document_tooling/065_2026-09-23T1425_write_the_new_closing_chapter_splice_everything_into_the_doc.txt |
| 066 | 2026-09-23 14:25 | Fix the wide table, recompile, and render the new pages for a layout check | document_tooling/066_2026-09-23T1425_fix_the_wide_table_recompile_and_render_the_new_pages_for_a_.txt |
| 107 | 2026-09-23 22:40 | Compile the LaTeX to PDF and check for errors | document_tooling/107_2026-09-23T2240_compile_the_latex_to_pdf_and_check_for_errors.txt |
| 108 | 2026-09-23 22:40 | Fix the overfull tables, recompile, and copy outputs | document_tooling/108_2026-09-23T2240_fix_the_overfull_tables_recompile_and_copy_outputs.txt |
| 109 | 2026-09-23 22:41 | Combine sample pages into one image for a visual check | document_tooling/109_2026-09-23T2241_combine_sample_pages_into_one_image_for_a_visual_check.txt |
| 112 | 2026-09-24 02:44 | Check for label and macro clashes before merging Part III into the main document | document_tooling/112_2026-09-24T0244_check_for_label_and_macro_clashes_before_merging_part_iii_in.txt |
| 113 | 2026-09-24 02:47 | Merge Part III and the tick chapter into the main document and revise Parts I–III per the note | document_tooling/113_2026-09-24T0247_merge_part_iii_and_the_tick_chapter_into_the_main_document_a.txt |
| 114 | 2026-09-24 02:48 | Fix the mismatch, rebuild the merged third edition, and compile it | document_tooling/114_2026-09-24T0248_fix_the_mismatch_rebuild_the_merged_third_edition_and_compil.txt |
| 115 | 2026-09-24 02:48 | Rebuild and compile the third edition, then check for errors and undefined references | document_tooling/115_2026-09-24T0248_rebuild_and_compile_the_third_edition_then_check_for_errors_.txt |
| 116 | 2026-09-24 02:48 | Locate the revised pages and render them for a visual check | document_tooling/116_2026-09-24T0248_locate_the_revised_pages_and_render_them_for_a_visual_check.txt |
| 117 | 2026-09-24 02:48 | Combine the postulate page and the new chapter pages for a visual check | document_tooling/117_2026-09-24T0248_combine_the_postulate_page_and_the_new_chapter_pages_for_a_v.txt |
| 118 | 2026-09-24 02:49 | Use the edited Part III text, rebuild, compile, and verify the edits took effect | document_tooling/118_2026-09-24T0249_use_the_edited_part_iii_text_rebuild_compile_and_verify_the_.txt |
| 119 | 2026-09-24 02:49 | Fix the last stale mention, recompile, and copy the third edition to outputs | document_tooling/119_2026-09-24T0249_fix_the_last_stale_mention_recompile_and_copy_the_third_edit.txt |
| 122 | 2026-09-24 03:08 | Revise the tick chapter: global synchronisation is the end of reality, and vanishing leaves a remainder and disturbs the field | document_tooling/122_2026-09-24T0308_revise_the_tick_chapter_global_synchronisation_is_the_end_of.txt |
| 123 | 2026-09-24 03:09 | Update the merged edition for the clarification and recompile | document_tooling/123_2026-09-24T0309_update_the_merged_edition_for_the_clarification_and_recompil.txt |
| 124 | 2026-09-24 03:09 | Apply the clarification edits to the merge pipeline correctly | document_tooling/124_2026-09-24T0309_apply_the_clarification_edits_to_the_merge_pipeline_correctl.txt |
| 125 | 2026-09-24 03:10 | Replace the summary-table line directly and inspect the remaining targets | document_tooling/125_2026-09-24T0310_replace_the_summary_table_line_directly_and_inspect_the_rema.txt |
| 126 | 2026-09-24 03:10 | Re-apply all clarification edits, rebuild and compile, and check nothing stale remains | document_tooling/126_2026-09-24T0310_re_apply_all_clarification_edits_rebuild_and_compile_and_che.txt |
| 127 | 2026-09-24 03:11 | Fix the wide table, recompile, and locate the revised sections | document_tooling/127_2026-09-24T0311_fix_the_wide_table_recompile_and_locate_the_revised_sections.txt |
| 128 | 2026-09-24 03:11 | Render the revised postulate and vanishing pages for a visual check | document_tooling/128_2026-09-24T0311_render_the_revised_postulate_and_vanishing_pages_for_a_visua.txt |
