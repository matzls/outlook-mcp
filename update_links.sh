#!/bin/bash

# Create necessary directories if they don't exist
mkdir -p ".cursor/rules"
mkdir -p ".roo/rules"
mkdir -p ".roo/rules-architect"
mkdir -p ".roo/rules-code"
mkdir -p ".roo/rules-debug"
mkdir -p ".clinerules/rules"
mkdir -p ".clinerules/PLAN"
mkdir -p ".clinerules/ACT"

# Remove existing symbolic links
find ".roo" -type l -delete 2>/dev/null
find ".clinerules" -type l -delete 2>/dev/null

# Create symbolic links for .roo directory
ln -s "../../.cursor/rules/rules.mdc" ".roo/rules/rules.mdc"
ln -s "../../.cursor/rules/memory.mdc" ".roo/rules/memory.mdc"
ln -s "../../.cursor/rules/directory-structure.mdc" ".roo/rules/directory-structure.mdc"

ln -s "../../.cursor/rules/plan.mdc" ".roo/rules-architect/plan.mdc"
ln -s "../../.cursor/rules/architecture-understanding.mdc" ".roo/rules-architect/architecture-understanding.mdc"

ln -s "../../.cursor/rules/implement.mdc" ".roo/rules-code/implement.mdc"
ln -s "../../.cursor/rules/testing.mdc" ".roo/rules-code/testing.mdc"

ln -s "../../.cursor/rules/debug.mdc" ".roo/rules-debug/debug.mdc"

# Create symbolic links for .clinerules directory
ln -s "../../.cursor/rules/rules.mdc" ".clinerules/rules/rules.mdc"
ln -s "../../.cursor/rules/memory.mdc" ".clinerules/rules/memory.mdc"
ln -s "../../.cursor/rules/directory-structure.mdc" ".clinerules/rules/directory-structure.mdc"

ln -s "../../.cursor/rules/plan.mdc" ".clinerules/PLAN/plan.mdc"

ln -s "../../.cursor/rules/implement.mdc" ".clinerules/ACT/implement.mdc"
ln -s "../../.cursor/rules/debug.mdc" ".clinerules/ACT/debug.mdc"

echo "All symbolic links have been updated to point to .cursor/rules."
