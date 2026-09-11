import matrixData from '../data/taxonomy_matrix.json';
import { ServiceInfo, NicheInfo, TechStackInfo, LocationInfo, CombinationRecord } from '../types/pseo';

export function getTaxonomyDimensions() {
  return matrixData.taxonomy_dimensions;
}

export function getAllServices(): ServiceInfo[] {
  return matrixData.taxonomy_dimensions.services as ServiceInfo[];
}

export function getAllNiches(): NicheInfo[] {
  return matrixData.taxonomy_dimensions.niches as NicheInfo[];
}

export function getAllTechStacks(): TechStackInfo[] {
  return matrixData.taxonomy_dimensions.tech_stacks as TechStackInfo[];
}

export function getAllLocations(): LocationInfo[] {
  return matrixData.taxonomy_dimensions.locations as LocationInfo[];
}

export function getAllCombinations(): CombinationRecord[] {
  return matrixData.combinations as CombinationRecord[];
}

export function getNicheBySlug(slugPart: string): NicheInfo | undefined {
  const clean = slugPart.toLowerCase().trim();
  return getAllNiches().find(
    n => n.id === clean || n.slug_part === clean || n.id.replace(/-/g, '') === clean.replace(/-/g, '')
  );
}

export function getServiceBySlug(slugPart: string): ServiceInfo | undefined {
  const clean = slugPart.toLowerCase().trim();
  return getAllServices().find(
    s => s.id === clean || s.slug_part === clean || s.id.replace(/-/g, '') === clean.replace(/-/g, '')
  );
}

export function findCombination(nicheSlug: string, serviceSlug: string): CombinationRecord | undefined {
  const niche = getNicheBySlug(nicheSlug);
  const service = getServiceBySlug(serviceSlug);
  if (!niche || !service) return undefined;

  return getAllCombinations().find(
    c => (c.niche.id === niche.id || c.niche.name.toLowerCase().includes(niche.id.toLowerCase())) &&
         (c.service.id === service.id || c.service.short_name.toLowerCase().includes(service.id.toLowerCase()))
  );
}
