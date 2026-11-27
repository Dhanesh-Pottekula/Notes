#!/bin/bash
# run_all.sh - run every practice script on the sample files in ../fixtures.
# Each command and its output is saved in ../src/out/<name>.txt (the guide pages show these files).
cd "$(dirname "$0")" || exit 1
F=../fixtures
OUT=../src/out
mkdir -p "$OUT"
run() {                       # run <name> <command...>
    local name=$1; shift
    { echo "\$ $*"; "$@" 2>&1; echo "[exit code $?]"; } > "$OUT/$name.txt"
    cat "$OUT/$name.txt"; echo
}
run drc_summary_pl  perl drc_summary.pl  $F/top.drc.summary
run drc_compare_pl  perl drc_compare.pl  $F/prev.drc.summary $F/top.drc.summary
run drc_waive_pl    perl drc_waive.pl    $F/top.drc.summary $F/waivers.txt
run rdb_bbox_pl     perl rdb_bbox.pl     $F/top.drc.results
run rdb_hotspot_pl  perl rdb_hotspot.pl  $F/top.drc.results 20
run lvs_triage_pl   perl lvs_triage.pl   $F/top.lvs.report
run cdl_ports_pl    perl cdl_ports.pl    $F/src.cdl $F/lay.cdl
run log_scan_pl     perl log_scan.pl     $F/logs/blkA.drc.log $F/logs/blkB.drc.log $F/logs/blkC.drc.log
if command -v tclsh >/dev/null; then
    run pvlib_test_tcl   tclsh pvlib_test.tcl
    run drc_summary_tcl  tclsh drc_summary.tcl  $F/top.drc.summary
    run gen_runs_tcl     tclsh gen_runs.tcl     $F/blocks.list $OUT/demo_runs
    run layermap_tcl     tclsh layermap_check.tcl $F/layer.map $F/required_layers.txt
    run cell_diff_tcl    tclsh cell_diff.tcl    $F/gds_cells.txt $F/lef_cells.txt
    run rdb_to_tcl_tcl   tclsh rdb_to_tcl.tcl   $F/top.drc.results $OUT/demo_viol.tcl
fi
